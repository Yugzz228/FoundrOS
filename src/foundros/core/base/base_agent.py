"""BaseAgent interface."""

from abc import ABC, abstractmethod
from typing import List, Optional
from foundros.models.message import Message
from foundros.models.idea import StartupIdea

class BaseAgent(ABC):
    """
    The abstract base class for all autonomous participants in FoundrOS.
    """
    
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description
        self.memory: List[Message] = []
        
    @abstractmethod
    def execute(self, idea: StartupIdea, context: Optional[List[Message]] = None) -> Message:
        """
        Execute the agent's primary function based on the startup idea and current context.
        
        Args:
            idea: The user's startup idea.
            context: A list of messages representing the conversation or work history.
            
        Returns:
            A Message containing the agent's output.
        """
        pass
