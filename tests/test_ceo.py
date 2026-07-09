"""Tests for the CEO Agent."""

import pytest
from foundros.agents.ceo import CEOAgent
from foundros.models.idea import StartupIdea
from foundros.services.llm import LLMService

class MockLLMService(LLMService):
    def __init__(self):
        pass
        
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return (
            "- CTO: Database Architecture - Design the schema for user data.\n"
            "- PM: PRD - Write the requirements document.\n"
            "- CFO: Cost Analysis - Estimate AWS costs.\n"
            "- Invalid: Format - Should be ignored"
        )

def test_ceo_agent_parsing():
    mock_llm = MockLLMService()
    ceo = CEOAgent(llm_service=mock_llm)
    
    idea = StartupIdea(title="TestApp", description="A test application")
    result = ceo.execute(idea)
    
    assert result.role == "assistant"
    assert result.agent_name == "CEO"
    
    # Test the internal parser
    tasks = ceo._parse_tasks(result.content)
    assert len(tasks) == 3
    
    assert tasks[0].assignee_role == "CTO"
    assert tasks[0].title == "Database Architecture"
    assert tasks[0].description == "Design the schema for user data."
    
    assert tasks[1].assignee_role == "PM"
    assert tasks[2].assignee_role == "CFO"
