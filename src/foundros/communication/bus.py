"""Event Bus for asynchronous agent communication."""

import asyncio
import logging
from typing import Dict, List, Callable, Awaitable, Any

logger = logging.getLogger(__name__)

# Callback type: takes an event payload (dict or object) and returns Awaitable
EventHandler = Callable[[Any], Awaitable[None]]

class EventBus:
    """A simple Pub/Sub event bus using asyncio."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[EventHandler]] = {}
        
    def subscribe(self, event_type: str, handler: EventHandler):
        """Subscribe a handler to a specific event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        logger.debug(f"Subscribed to {event_type}")

    async def publish(self, event_type: str, payload: Any):
        """Publish an event to all subscribers."""
        logger.info(f"EventBus: Publishing [{event_type}]")
        if event_type in self.subscribers:
            handlers = self.subscribers[event_type]
            # Execute all handlers for this event concurrently
            await asyncio.gather(*(handler(payload) for handler in handlers))
        else:
            logger.debug(f"No subscribers for event: {event_type}")
