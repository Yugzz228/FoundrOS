"""Tests for the generic Executive Agent."""

import pytest
from foundros.models.idea import StartupIdea
from foundros.models.task import Task
from foundros.models.message import Message
from foundros.services.llm import AsyncLLMService
from foundros.agents.executive import ExecutiveAgent

class MockAsyncLLMService(AsyncLLMService):
    def __init__(self):
        pass
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return "Mock response"

@pytest.mark.asyncio
async def test_executive_agent_factory():
    llm = MockAsyncLLMService()
    idea = StartupIdea(title="Test", description="Test Idea")
    task = Task(title="Test Task", description="Do something", assignee_role="CTO")
    
    cto = ExecutiveAgent("CTO", "Chief Technology Officer", "cto.md", llm)
    msg = await cto.execute(idea, task=task)
    assert msg.agent_name == "CTO"
    assert msg.content == "Mock response"
