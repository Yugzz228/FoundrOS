"""CEO Agent implementation."""

import os
from typing import List, Optional, Any
from foundros.core.base.base_agent import BaseAgent
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.models.task import Task
from foundros.models.delegation import DelegationPlan
from foundros.services.llm import AsyncLLMService

class CEOAgent(BaseAgent):
    """The Chief Executive Officer agent."""
    
    def __init__(self, llm_service: AsyncLLMService):
        super().__init__(name="CEO", role_description="Chief Executive Officer")
        self.llm_service = llm_service
        self.prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "ceo.md")
        
    def _load_prompt(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    async def execute(self, idea: StartupIdea, context: Optional[List[Message]] = None, task: Optional['Task'] = None) -> DelegationPlan:
        system_prompt = self._load_prompt()
        user_prompt = f"Startup Idea: {idea.title}\nDescription: {idea.description}\nIndustry: {idea.industry or 'Unknown'}"
        
        # We use strict structured parsing here to get a DelegationPlan object directly
        plan = await self.llm_service.generate_structured_response(system_prompt, user_prompt, DelegationPlan)
        return plan
