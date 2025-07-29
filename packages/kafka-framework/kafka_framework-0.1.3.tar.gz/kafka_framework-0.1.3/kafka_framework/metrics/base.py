from abc import ABC, abstractmethod
from typing import Optional


class MetricsCollector(ABC):
    """Base class for metrics collectors."""

    @abstractmethod
    def record_message_processed(
            self,
            topic: str,
            status: str = "success",
            duration: Optional[float] = None,
            **labels: str,
    ) -> None:
        """Record a message processing event."""
        pass

    @abstractmethod
    def record_error(self, error_type: str, topic: str, **labels: str) -> None:
        """Record an error event."""
        pass

    @abstractmethod
    def record_latency(self, metric_name: str, duration: float, **labels: str) -> None:
        """Record a latency measurement."""
        pass
