"""Memory Management for context windows."""

import logging
from typing import List
from foundros.models.message import Message
from foundros.services.llm import AsyncLLMService

logger = logging.getLogger(__name__)

class MemoryManager:
    """Manages a sliding window of context and summarizes older messages."""
    
    def __init__(self, llm_service: AsyncLLMService, max_messages: int = 10):
        self.llm_service = llm_service
        self.max_messages = max_messages
        self.buffer: List[Message] = []
        self.summary: str = ""
        
    def add_message(self, message: Message):
        self.buffer.append(message)
        
    def get_context(self) -> List[Message]:
        """Returns the current context window, optionally prepended with a summary."""
        context = []
        if self.summary:
            context.append(Message(role="system", content=f"Previous Context Summary: {self.summary}"))
        context.extend(self.buffer)
        return context
        
    async def compress_if_needed(self):
        """If buffer exceeds max_messages, compress the oldest messages."""
        if len(self.buffer) > self.max_messages:
            logger.info("MemoryManager: Compressing memory buffer...")
            # We compress the oldest half of the messages
            split_index = len(self.buffer) // 2
            old_messages = self.buffer[:split_index]
            
            prompt = "Summarize the following execution history strictly and concisely:\n"
            for msg in old_messages:
                agent = msg.agent_name or msg.role
                prompt += f"[{agent}]: {msg.content}\n"
                
            new_summary = await self.llm_service.generate_response(
                system_prompt="You are an expert technical summarizer.",
                user_prompt=prompt
            )
            
            # Update summary and truncate buffer
            if self.summary:
                self.summary = f"{self.summary}\nThen, {new_summary}"
            else:
                self.summary = new_summary
                
            self.buffer = self.buffer[split_index:]
            logger.info("MemoryManager: Compression complete.")
