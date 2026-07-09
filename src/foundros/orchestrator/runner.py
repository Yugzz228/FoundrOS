"""Synchronous workflow orchestrator for Prototype v1.0."""

import logging
from typing import List, Dict
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.services.llm import LLMService
from foundros.agents.ceo import CEOAgent
from foundros.agents.executive import ExecutiveAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    """Runs the full FoundrOS simulation pipeline."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.ceo = CEOAgent(llm_service)
        
        # Factory instantiated executives
        self.executives = {
            "CTO": ExecutiveAgent("CTO", "Chief Technology Officer", "cto.md", llm_service),
            "PM": ExecutiveAgent("PM", "Product Manager", "pm.md", llm_service),
            "CFO": ExecutiveAgent("CFO", "Chief Financial Officer", "cfo.md", llm_service)
        }
        self.investor = ExecutiveAgent("Investor", "Venture Capitalist", "investor.md", llm_service)
        
        self.context: List[Message] = []
        
    def run(self, idea: StartupIdea) -> str:
        """Executes the full simulation given a startup idea."""
        logger.info(f"Starting FoundrOS simulation for: {idea.title}")
        
        # Step 1: CEO breaks down tasks
        logger.info("CEO is analyzing the idea and delegating tasks...")
        ceo_message = self.ceo.execute(idea)
        self.context.append(ceo_message)
        
        # The CEO agent parses tasks internally. We can retrieve them.
        tasks = self.ceo._parse_tasks(ceo_message.content)
        logger.info(f"CEO generated {len(tasks)} tasks.")
        
        # Step 2: Executives execute their tasks
        for task in tasks:
            if task.assignee_role in self.executives:
                agent = self.executives[task.assignee_role]
                logger.info(f"{task.assignee_role} is executing task: {task.title}")
                msg = agent.execute(idea, context=self.context, task=task)
                self.context.append(msg)
            else:
                logger.warning(f"Unknown assignee role: {task.assignee_role}")
                
        # Step 3: Investor reviews the final output
        logger.info("Investor is reviewing the final output...")
        investor_message = self.investor.execute(idea, context=self.context)
        self.context.append(investor_message)
        
        # Step 4: Compile the final report
        logger.info("Simulation complete. Compiling report.")
        return self._generate_report(idea)
        
    def _generate_report(self, idea: StartupIdea) -> str:
        report = [
            f"# FoundrOS Executive Report: {idea.title}",
            f"**Industry:** {idea.industry or 'N/A'}",
            f"**Description:** {idea.description}",
            "---"
        ]
        
        for msg in self.context:
            role_header = f"## {msg.agent_name or msg.role.capitalize()}"
            report.append(role_header)
            report.append(msg.content)
            report.append("---")
            
        return "\n\n".join(report)
