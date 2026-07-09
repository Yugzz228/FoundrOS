"""Tests for the Orchestrator."""

import pytest
from foundros.models.idea import StartupIdea
from foundros.services.llm import LLMService
from foundros.orchestrator.runner import Orchestrator

class MockLLMService(LLMService):
    def __init__(self):
        pass
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        # Mocking the CEO specifically to generate tasks so the loop executes
        if "Chief Executive Officer" in system_prompt:
            return (
                "- CTO: Database - Design schema\n"
                "- PM: PRD - Write features\n"
            )
        return "Mock execution output."

def test_orchestrator_run():
    llm = MockLLMService()
    orchestrator = Orchestrator(llm_service=llm)
    
    idea = StartupIdea(title="Test", description="Test Idea", industry="Tech")
    
    report = orchestrator.run(idea)
    
    assert "FoundrOS Executive Report: Test" in report
    assert "Mock execution output." in report
    
    # The context should contain CEO, CTO, PM, and Investor messages
    agent_names = [msg.agent_name for msg in orchestrator.context]
    assert "CEO" in agent_names
    assert "CTO" in agent_names
    assert "PM" in agent_names
    assert "CFO" not in agent_names # CEO didn't delegate to CFO in mock
    assert "Investor" in agent_names
