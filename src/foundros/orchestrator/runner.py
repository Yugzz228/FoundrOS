"""Asynchronous Event-Driven workflow orchestrator for Prototype v2.0."""

import asyncio
import logging
from typing import List, Any
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.models.task import Task
from foundros.services.llm import AsyncLLMService
from foundros.agents.ceo import CEOAgent
from foundros.agents.executive import ExecutiveAgent
from foundros.communication.bus import EventBus
from foundros.memory.buffer import MemoryManager

logger = logging.getLogger(__name__)

class Orchestrator:
    """Runs the full FoundrOS simulation pipeline asynchronously."""
    
    def __init__(self, llm_service: AsyncLLMService):
        self.llm_service = llm_service
        self.bus = EventBus()
        self.memory = MemoryManager(llm_service, max_messages=15)
        
        # Instantiate Agents
        self.ceo = CEOAgent(llm_service)
        self.executives = {
            "CTO": ExecutiveAgent("CTO", "Chief Technology Officer", "cto.md", llm_service),
            "PM": ExecutiveAgent("PM", "Product Manager", "pm.md", llm_service),
            "CFO": ExecutiveAgent("CFO", "Chief Financial Officer", "cfo.md", llm_service)
        }
        self.investor = ExecutiveAgent("Investor", "Venture Capitalist", "investor.md", llm_service)
        
        # State tracking
        self.active_tasks = 0
        self.simulation_complete_event = asyncio.Event()
        self.final_report = ""
        
        # Setup Event Subscriptions
        self._setup_subscriptions()
        
    def _setup_subscriptions(self):
        self.bus.subscribe("IdeaSubmitted", self._handle_idea_submitted)
        self.bus.subscribe("TasksDelegated", self._handle_tasks_delegated)
        self.bus.subscribe("ExecutiveTaskCompleted", self._handle_executive_completed)
        self.bus.subscribe("AllTasksCompleted", self._handle_all_tasks_completed)
        
    async def run(self, idea: StartupIdea) -> str:
        """Starts the event-driven simulation and waits for completion."""
        logger.info(f"Starting async FoundrOS simulation for: {idea.title}")
        
        # Kick off the event pipeline
        await self.bus.publish("IdeaSubmitted", idea)
        
        # Wait until the investor finishes and triggers the complete event
        await self.simulation_complete_event.wait()
        return self.final_report

    async def _handle_idea_submitted(self, idea: StartupIdea):
        logger.info("CEO is analyzing the idea and generating structured tasks...")
        plan = await self.ceo.execute(idea)
        
        # We store CEO's output as a system message in memory
        tasks_str = "\n".join([f"- {t.assignee_role}: {t.title}" for t in plan.tasks])
        msg = Message(role="assistant", agent_name="CEO", content=f"Delegated Tasks:\n{tasks_str}")
        self.memory.add_message(msg)
        
        logger.info(f"CEO generated {len(plan.tasks)} tasks.")
        await self.bus.publish("TasksDelegated", {"idea": idea, "tasks": plan.tasks})

    async def _handle_tasks_delegated(self, payload: dict):
        idea = payload["idea"]
        tasks: List[Task] = payload["tasks"]
        self.active_tasks = len(tasks)
        
        # Execute all executives in parallel
        async def _run_agent(task: Task):
            if task.assignee_role in self.executives:
                agent = self.executives[task.assignee_role]
                logger.info(f"{task.assignee_role} is executing task: {task.title}")
                msg = await agent.execute(idea, context=self.memory.get_context(), task=task)
                await self.bus.publish("ExecutiveTaskCompleted", msg)
            else:
                logger.warning(f"Unknown assignee role: {task.assignee_role}")
                self.active_tasks -= 1

        # Fire and forget the tasks concurrently
        await asyncio.gather(*(_run_agent(task) for task in tasks))

    async def _handle_executive_completed(self, msg: Message):
        self.memory.add_message(msg)
        self.active_tasks -= 1
        logger.info(f"{msg.agent_name} completed their task. {self.active_tasks} tasks remaining.")
        
        await self.memory.compress_if_needed()
        
        if self.active_tasks <= 0:
            await self.bus.publish("AllTasksCompleted", None)

    async def _handle_all_tasks_completed(self, payload: Any):
        logger.info("All tasks completed. Investor is reviewing...")
        dummy_idea = StartupIdea(title="Final Review", description="Reviewing output")
        
        investor_msg = await self.investor.execute(dummy_idea, context=self.memory.get_context())
        self.memory.add_message(investor_msg)
        
        logger.info("Simulation complete. Compiling report.")
        self.final_report = self._generate_report()
        self.simulation_complete_event.set()

    def _generate_report(self) -> str:
        report = ["# FoundrOS Final Executive Report", "---"]
        if self.memory.summary:
            report.append(f"**Context Summary:**\n{self.memory.summary}\n---")
            
        for msg in self.memory.buffer:
            role_header = f"## {msg.agent_name or msg.role.capitalize()}"
            report.append(role_header)
            report.append(msg.content)
            report.append("---")
            
        return "\n\n".join(report)
