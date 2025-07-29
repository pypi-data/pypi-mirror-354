from typing import Any, Callable, List, Optional, TypeVar
from dataclasses import dataclass
from enum import Enum

# Type variables for generic type hints
T = TypeVar("T")
MessageT = TypeVar("MessageT")

# Message handler type
HandlerFunc = Callable[["MessageContext"], Any]

# Middleware type
MiddlewareFunc = Callable[["MessageContext", HandlerFunc], Any]


class MessagePriority(Enum):
    """Standard priority levels for message processing"""

    HIGH = 100
    NORMAL = 10
    LOW = 1


@dataclass
class TopicConfig:
    """Configuration for a Kafka topic subscription"""

    name: str
    handler: HandlerFunc
    priority: int = MessagePriority.NORMAL.value
    auto_commit: bool = True


@dataclass
class ConsumerConfig:
    """Configuration for Kafka consumer"""

    bootstrap_servers: List[str]
    group_id: Optional[str] = None
    enable_auto_commit: bool = True
    auto_offset_reset: str = "earliest"
    session_timeout_ms: int = 10000
    heartbeat_interval_ms: int = 3000


# Default configuration values
DEFAULT_CONSUMER_CONFIG = ConsumerConfig(bootstrap_servers=["localhost:9092"])

# Common constants
MAX_POLL_RECORDS = 500
MAX_POLL_INTERVAL_MS = 300000
REQUEST_TIMEOUT_MS = 40000
SESSION_TIMEOUT_MS = 10000
HEARTBEAT_INTERVAL_MS = 3000
