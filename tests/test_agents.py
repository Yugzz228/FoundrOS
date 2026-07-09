"""Tests for the generic Executive Agent."""

import pytest
from foundros.models.idea import StartupIdea
from foundros.models.task import Task
from foundros.models.message import Message
from foundros.services.llm import LLMService
from foundros.agents.executive import ExecutiveAgent

class MockLLMService(LLMService):
    def __init__(self):
        pass
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return "Mock response"

def test_executive_agent_factory():
    llm = MockLLMService()
    idea = StartupIdea(title="Test", description="Test Idea")
    task = Task(title="Test Task", description="Do something", assignee_role="CTO")
    
    # Test CTO
    cto = ExecutiveAgent("CTO", "Chief Technology Officer", "cto.md", llm)
    msg = cto.execute(idea, task=task)
    assert msg.agent_name == "CTO"
    assert msg.content == "Mock response"
    
    # Test Investor with context
    context = [Message(role="assistant", content="CTO Report", agent_name="CTO")]
    investor = ExecutiveAgent("Investor", "Venture Capitalist", "investor.md", llm)
    msg = investor.execute(idea, context=context)
    assert msg.agent_name == "Investor"
