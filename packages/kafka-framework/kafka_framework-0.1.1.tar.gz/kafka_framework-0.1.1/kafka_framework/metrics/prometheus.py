from typing import Optional
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from . import MetricsCollector


class PrometheusMetrics(MetricsCollector):
    """Prometheus metrics collector for Kafka framework."""

    def __init__(self, port: int = 8000, addr: str = "0.0.0.0"):
        self.port = port
        self.addr = addr

        # Message processing metrics
        self.messages_processed = Counter(
            "kafka_messages_processed_total",
            "Total number of messages processed",
            ["topic", "status"],
        )

        # Error metrics
        self.errors = Counter(
            "kafka_processing_errors_total",
            "Total number of processing errors",
            ["error_type", "topic"],
        )

        # Processing time histogram
        self.processing_time = Histogram(
            "kafka_message_processing_seconds",
            "Time spent processing messages",
            ["topic"],
            buckets=(
                0.001,
                0.005,
                0.01,
                0.05,
                0.1,
                0.5,
                1.0,
                2.5,
                5.0,
                10.0,
                float("inf"),
            ),
        )

        # Consumer lag gauge
        self.consumer_lag = Gauge(
            "kafka_consumer_lag", "Current consumer lag", ["topic", "partition"]
        )

        # Start metrics server
        start_http_server(port, addr=addr)

    def record_message_processed(
        self,
        topic: str,
        status: str = "success",
        duration: Optional[float] = None,
        **labels: str,
    ) -> None:
        """Record a message processing event."""
        self.messages_processed.labels(topic=topic, status=status).inc()
        if duration is not None:
            self.processing_time.labels(topic=topic).observe(duration)

    def record_error(self, error_type: str, topic: str, **labels: str) -> None:
        """Record an error event."""
        self.errors.labels(error_type=error_type, topic=topic).inc()

    def record_latency(self, metric_name: str, duration: float, **labels: str) -> None:
        """Record a latency measurement."""
        # For Prometheus, we'll use a histogram for all latencies
        Histogram(
            f"kafka_{metric_name}_seconds",
            f"Time spent in {metric_name}",
            list(labels.keys()),
            buckets=(
                0.001,
                0.005,
                0.01,
                0.05,
                0.1,
                0.5,
                1.0,
                2.5,
                5.0,
                10.0,
                float("inf"),
            ),
        ).labels(**labels).observe(duration)

    def update_consumer_lag(self, topic: str, partition: int, lag: int) -> None:
        """Update the consumer lag metric."""
        self.consumer_lag.labels(topic=topic, partition=partition).set(lag)
