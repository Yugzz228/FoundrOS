"""Startup Idea domain model."""

from pydantic import BaseModel, Field

class StartupIdea(BaseModel):
    """Represents a startup idea inputted by the user."""
    title: str = Field(..., description="The name or title of the startup idea")
    description: str = Field(..., description="A detailed description of the startup idea")
    industry: str | None = Field(None, description="The industry or market category")
