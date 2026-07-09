"""Tests for all executive agents."""

import pytest
from foundros.models.idea import StartupIdea
from foundros.models.task import Task
from foundros.models.message import Message
from foundros.services.llm import LLMService
from foundros.agents.cto import CTOAgent
from foundros.agents.pm import PMAgent
from foundros.agents.cfo import CFOAgent
from foundros.agents.investor import InvestorAgent

class MockLLMService(LLMService):
    def __init__(self):
        pass
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        return "Mock response"

def test_executive_agents_execution():
    llm = MockLLMService()
    idea = StartupIdea(title="Test", description="Test Idea")
    task = Task(title="Test Task", description="Do something", assignee_role="CTO")
    
    cto = CTOAgent(llm)
    msg = cto.execute(idea, task=task)
    assert msg.agent_name == "CTO"
    assert msg.content == "Mock response"
    
    pm = PMAgent(llm)
    msg = pm.execute(idea, task=task)
    assert msg.agent_name == "PM"
    
    cfo = CFOAgent(llm)
    msg = cfo.execute(idea, task=task)
    assert msg.agent_name == "CFO"
    
    # Investor testing with context
    context = [Message(role="assistant", content="CTO Report", agent_name="CTO")]
    investor = InvestorAgent(llm)
    msg = investor.execute(idea, context=context)
    assert msg.agent_name == "Investor"
