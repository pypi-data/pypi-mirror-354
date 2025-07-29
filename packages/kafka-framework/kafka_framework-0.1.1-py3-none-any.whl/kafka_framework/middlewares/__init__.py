"""Middleware implementations for the Kafka framework."""

from typing import Any, Callable, Optional
from kafka_framework.types import MessageContext, MiddlewareFunc


class BaseMiddleware:
    """Base class for all middleware implementations."""

    def __init__(self, **kwargs):
        self.config = kwargs

    async def __call__(self, ctx: MessageContext, call_next: Callable) -> Any:
        """Process the message and call the next middleware in the chain."""
        return await call_next(ctx)


# Import built-in middlewares
from .logging_middleware import LoggingMiddleware
from .retry_middleware import RetryMiddleware

__all__ = [
    "BaseMiddleware",
    "LoggingMiddleware",
    "RetryMiddleware",
]
