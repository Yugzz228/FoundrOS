"""CEO Agent implementation."""

import os
from typing import List, Optional
from foundros.core.base.base_agent import BaseAgent
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.models.task import Task
from foundros.services.llm import LLMService

class CEOAgent(BaseAgent):
    """The CEO Agent responsible for delegating tasks based on a startup idea."""
    
    def __init__(self, llm_service: LLMService):
        super().__init__(name="CEO", role_description="Chief Executive Officer")
        self.llm_service = llm_service
        self.prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "ceo.md")
        
    def _load_prompt(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()
            
    def _parse_tasks(self, llm_output: str) -> List[Task]:
        """Simple parser to extract tasks from the LLM's markdown output."""
        tasks = []
        for line in llm_output.strip().split("\n"):
            line = line.strip()
            if line.startswith("- ") and ":" in line and "-" in line[line.find(":"):]:
                # Expected format: - ASSIGNEE: Title - Description
                try:
                    parts = line[2:].split(":", 1)
                    assignee = parts[0].strip()
                    desc_parts = parts[1].split("-", 1)
                    title = desc_parts[0].strip()
                    description = desc_parts[1].strip()
                    
                    if assignee in ["CTO", "PM", "CFO"]:
                        tasks.append(Task(
                            title=title,
                            description=description,
                            assignee_role=assignee
                        ))
                except Exception:
                    continue # Skip malformed lines for prototype simplicity
        return tasks

    def execute(self, idea: StartupIdea, context: Optional[List[Message]] = None, task: Optional['Task'] = None) -> Message:
        system_prompt = self._load_prompt()
        user_prompt = f"Startup Idea: {idea.title}\nDescription: {idea.description}\nIndustry: {idea.industry or 'Unknown'}"
        
        raw_response = self.llm_service.generate_response(system_prompt, user_prompt)
        
        # Parse the tasks to ensure we structured the output correctly
        # In a more advanced implementation, we would return these tasks along with the message.
        # For now, parsing them validates the LLM followed instructions.
        tasks = self._parse_tasks(raw_response)
        
        return Message(
            role="assistant",
            content=raw_response,
            agent_name=self.name
        )
