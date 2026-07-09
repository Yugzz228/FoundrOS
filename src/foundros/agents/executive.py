"""Generic Executive Agent implementation."""

import os
from typing import List, Optional
from foundros.core.base.base_agent import BaseAgent
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.models.task import Task
from foundros.services.llm import AsyncLLMService

class ExecutiveAgent(BaseAgent):
    """A generic, configuration-driven agent for executive roles."""
    
    def __init__(self, name: str, role_description: str, prompt_filename: str, llm_service: AsyncLLMService):
        super().__init__(name=name, role_description=role_description)
        self.llm_service = llm_service
        self.prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", prompt_filename)
        
    def _load_prompt(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    async def execute(self, idea: StartupIdea, context: Optional[List[Message]] = None, task: Optional[Task] = None) -> Message:
        system_prompt = self._load_prompt()
        
        user_prompt = f"Startup Idea: {idea.title}\nDescription: {idea.description}\n"
        if task:
            user_prompt += f"\nAssigned Task: {task.title}\nTask Details: {task.description}\n"
        if context:
            user_prompt += "\nAdditional Context:\n"
            for msg in context:
                agent_prefix = f"[{msg.agent_name}]" if msg.agent_name else f"[{msg.role}]"
                user_prompt += f"{agent_prefix}:\n{msg.content}\n\n"
                
        raw_response = await self.llm_service.generate_response(system_prompt, user_prompt)
        
        return Message(
            role="assistant",
            content=raw_response,
            agent_name=self.name
        )
