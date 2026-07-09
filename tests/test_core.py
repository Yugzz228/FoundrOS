"""Tests for core domain models and BaseAgent interface."""

import pytest
from pydantic import ValidationError
from foundros.models.idea import StartupIdea
from foundros.models.message import Message
from foundros.core.base.base_agent import BaseAgent

def test_startup_idea_validation():
    # Valid idea
    idea = StartupIdea(title="FoundrOS", description="AI Startup OS")
    assert idea.title == "FoundrOS"
    
    # Invalid idea (missing required fields)
    with pytest.raises(ValidationError):
        StartupIdea(title="FoundrOS")

def test_message_validation():
    msg = Message(role="user", content="Hello")
    assert msg.role == "user"
    
    with pytest.raises(ValidationError):
        Message(role="invalid_role", content="Hi")

def test_base_agent_interface():
    # Instantiating abstract class directly should fail
    with pytest.raises(TypeError):
        BaseAgent(name="Test", role_description="Testing")
        
    class MockAgent(BaseAgent):
        def execute(self, idea: StartupIdea, context=None) -> Message:
            return Message(role="assistant", content=f"Processed: {idea.title}", agent_name=self.name)
            
    agent = MockAgent(name="MockCEO", role_description="Test CEO")
    idea = StartupIdea(title="TestApp", description="Test")
    result = agent.execute(idea)
    
    assert result.content == "Processed: TestApp"
    assert result.agent_name == "MockCEO"
