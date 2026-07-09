"""Message domain model."""

from pydantic import BaseModel, Field
from typing import Literal

class Message(BaseModel):
    """Represents a message sent to or from an agent."""
    role: Literal["system", "user", "assistant"] = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The text content of the message")
    agent_name: str | None = Field(None, description="The name of the agent if role is assistant")
