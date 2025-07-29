"""Kafka Framework - A FastAPI-inspired framework for Kafka consumers."""

from .app import KafkaApp
from .router import TopicRouter
from .context import MessageContext
from .middleware import MiddlewareManager
from .config import Settings

__version__ = "0.1.0"

__all__ = [
    "KafkaApp",
    "TopicRouter",
    "MessageContext",
    "MiddlewareManager",
    "Settings",
]
