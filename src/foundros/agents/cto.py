"""CTO Agent implementation."""

import os
from typing import List, Optional
from foundros.core.base.base_agent import BaseAgent
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.models.task import Task
from foundros.services.llm import LLMService

class CTOAgent(BaseAgent):
    """The CTO Agent responsible for technical architecture and stack choices."""
    
    def __init__(self, llm_service: LLMService):
        super().__init__(name="CTO", role_description="Chief Technology Officer")
        self.llm_service = llm_service
        self.prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "cto.md")
        
    def _load_prompt(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def execute(self, idea: StartupIdea, context: Optional[List[Message]] = None, task: Optional[Task] = None) -> Message:
        system_prompt = self._load_prompt()
        
        user_prompt = f"Startup Idea: {idea.title}\nDescription: {idea.description}\n"
        if task:
            user_prompt += f"\nAssigned Task: {task.title}\nTask Details: {task.description}\n"
        if context:
            user_prompt += "\nAdditional Context:\n"
            for msg in context:
                user_prompt += f"[{msg.role}]: {msg.content}\n"
                
        raw_response = self.llm_service.generate_response(system_prompt, user_prompt)
        
        return Message(
            role="assistant",
            content=raw_response,
            agent_name=self.name
        )
