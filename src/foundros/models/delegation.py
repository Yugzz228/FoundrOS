from pydantic import BaseModel
from typing import List
from foundros.models.task import Task

class DelegationPlan(BaseModel):
    """The structured output from the CEO containing multiple tasks."""
    tasks: List[Task]
