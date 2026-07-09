"""LLM Service wrapper for FoundrOS."""

from typing import TypeVar, Type, Optional
from pydantic import BaseModel
from openai import AsyncOpenAI

T = TypeVar('T', bound=BaseModel)

class AsyncLLMService:
    """A wrapper for interacting with Async LLM providers."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generates a standard string response."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content or ""
        
    async def generate_structured_response(self, system_prompt: str, user_prompt: str, response_model: Type[T]) -> T:
        """Generates a strictly structured response using a Pydantic model."""
        response = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=response_model
        )
        return response.choices[0].message.parsed
