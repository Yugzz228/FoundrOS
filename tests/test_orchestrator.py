"""Tests for the Async Orchestrator."""

import pytest
from typing import TypeVar, Type
from pydantic import BaseModel
from foundros.models.idea import StartupIdea
from foundros.models.task import Task
from foundros.models.delegation import DelegationPlan
from foundros.services.llm import AsyncLLMService
from foundros.orchestrator.runner import Orchestrator

T = TypeVar('T', bound=BaseModel)

class MockAsyncLLMService(AsyncLLMService):
    def __init__(self):
        pass
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return "Mock execution output."
        
    async def generate_structured_response(self, system_prompt: str, user_prompt: str, response_model: Type[T]) -> T:
        plan = DelegationPlan(tasks=[
            Task(title="DB", description="Design DB", assignee_role="CTO"),
            Task(title="PRD", description="Write PRD", assignee_role="PM")
        ])
        return plan # type: ignore

@pytest.mark.asyncio
async def test_async_orchestrator_run():
    llm = MockAsyncLLMService()
    orchestrator = Orchestrator(llm_service=llm)
    
    idea = StartupIdea(title="Test", description="Test Idea", industry="Tech")
    report = await orchestrator.run(idea)
    
    assert "FoundrOS Final Executive Report" in report
    assert "Mock execution output." in report
    assert "CTO" in report
    assert "PM" in report
