from typing import Callable, Dict, List, TypeVar, Union, Optional

from .exceptions import KafkaFrameworkException

T = TypeVar("T")

HandlerFunc = Callable[[T], Union[None, T]]


class TopicRouter:
    def __init__(self):
        self._handlers: Dict[str, HandlerFunc] = {}
        self._topic_priorities: Dict[str, int] = {}

    def register_handler(
            self,
            topic: str,
            handler: HandlerFunc,
            priority: int = 1,
    ) -> None:
        """Register a handler function for a Kafka topic"""
        if topic in self._handlers:
            raise KafkaFrameworkException(
                f"Handler already registered for topic: {topic}"
            )

        self._handlers[topic] = handler
        self._topic_priorities[topic] = priority

    def get_handler(self, topic: str) -> Optional[HandlerFunc]:
        """Get handler function for a topic"""
        return self._handlers.get(topic)

    def get_all_topics(self) -> List[str]:
        """Get all registered topics"""
        return list(self._handlers.keys())

    def get_topic_priority(self, topic: str) -> int:
        """Get priority for a topic"""
        return self._topic_priorities.get(topic, 1)

    def kafka_handler(
            self,
            topic: str,
            priority: int = 1,
    ) -> Callable[[HandlerFunc], HandlerFunc]:
        """Decorator to register a Kafka handler"""

        def decorator(func: HandlerFunc) -> HandlerFunc:
            self.register_handler(topic, func, priority)
            return func

        return decorator
