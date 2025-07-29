from typing import Callable, Any

from kafka_framework import MessageContext


class BaseMiddleware:
    """Base class for all middleware implementations."""

    def __init__(self, **kwargs):
        self.config = kwargs

    async def __call__(self, ctx: MessageContext, call_next: Callable) -> Any:
        """Process the message and call the next middleware in the chain."""
        return await call_next(ctx)
