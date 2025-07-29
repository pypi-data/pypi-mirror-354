from typing import Optional
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource
from . import MetricsCollector


class OpenTelemetryMetrics(MetricsCollector):
    """OpenTelemetry metrics collector for Kafka framework."""

    def __init__(
        self, service_name: str = "kafka-framework", endpoint: Optional[str] = None
    ):
        # Create resource with service name
        resource = Resource(
            attributes={
                "service.name": service_name,
                "telemetry.sdk.language": "python",
            }
        )

        # Create metric readers
        readers = []

        # Add console exporter for local development
        console_exporter = ConsoleMetricExporter()
        readers.append(PeriodicExportingMetricReader(console_exporter))

        # TODO: Add OTLP exporter if endpoint is provided

        # Create and set the global meter provider
        provider = MeterProvider(resource=resource, metric_readers=readers)
        metrics.set_meter_provider(provider)

        # Create meters and instruments
        self.meter = metrics.get_meter("kafka.framework")

        # Message processing counter
        self.messages_processed = self.meter.create_counter(
            "kafka.messages.processed", description="Total number of messages processed"
        )

        # Error counter
        self.errors = self.meter.create_counter(
            "kafka.processing.errors", description="Total number of processing errors"
        )

        # Processing time histogram
        self.processing_time = self.meter.create_histogram(
            "kafka.message.processing.time",
            description="Time spent processing messages",
            unit="s",
        )

        # Consumer lag gauge
        self.consumer_lag = self.meter.create_observable_gauge(
            "kafka.consumer.lag", callbacks=[], description="Current consumer lag"
        )
        self._lag_values = {}

    def record_message_processed(
        self,
        topic: str,
        status: str = "success",
        duration: Optional[float] = None,
        **labels: str,
    ) -> None:
        """Record a message processing event."""
        attributes = {"topic": topic, "status": status, **labels}
        self.messages_processed.add(1, attributes)

        if duration is not None:
            self.processing_time.record(duration, attributes)

    def record_error(self, error_type: str, topic: str, **labels: str) -> None:
        """Record an error event."""
        attributes = {"error_type": error_type, "topic": topic, **labels}
        self.errors.add(1, attributes)

    def record_latency(self, metric_name: str, duration: float, **labels: str) -> None:
        """Record a latency measurement."""
        self.meter.create_histogram(
            f"kafka.{metric_name}.time",
            description=f"Time spent in {metric_name}",
            unit="s",
        ).record(duration, labels)

    def update_consumer_lag(self, topic: str, partition: int, lag: int) -> None:
        """Update the consumer lag metric."""
        key = (topic, partition)
        self._lag_values[key] = lag

        # Update the observable gauge
        def get_lag_callback():
            return [
                (value, {"topic": t, "partition": str(p)})
                for (t, p), value in self._lag_values.items()
            ]

        # Recreate the gauge with the updated callback
        self.consumer_lag = self.meter.create_observable_gauge(
            "kafka.consumer.lag",
            callbacks=[get_lag_callback],
            description="Current consumer lag",
        )
