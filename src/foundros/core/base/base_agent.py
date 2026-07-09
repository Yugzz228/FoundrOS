"""Base interface for all autonomous agents."""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.models.task import Task

class BaseAgent(ABC):
    """Abstract base class defining the standard interface for an Agent."""
    
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description
        self.memory: List[Message] = []
        
    @abstractmethod
    async def execute(self, idea: StartupIdea, context: Optional[List[Message]] = None, task: Optional['Task'] = None) -> Any:
        """
        Asynchronously execute the agent's primary function.
        Returns a Message or a list of Tasks.
        """
        pass
