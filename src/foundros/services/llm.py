"""LLM Service wrapper."""

import os
from openai import OpenAI

class LLMService:
    """A simple synchronous wrapper around the OpenAI client."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        # Uses OPENAI_API_KEY from environment if not explicitly provided
        self.client = OpenAI(api_key=api_key)
        self.model = model
        
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a text response from the LLM.
        
        Args:
            system_prompt: The agent's core instructions.
            user_prompt: The specific task or context for this execution.
            
        Returns:
            The raw string response from the LLM.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
