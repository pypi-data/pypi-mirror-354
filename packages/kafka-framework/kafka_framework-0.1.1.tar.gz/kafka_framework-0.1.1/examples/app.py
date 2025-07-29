import asyncio
import logging
import signal
from typing import Any, Dict

from kafka_framework import KafkaApp, TopicRouter, MessageContext
from kafka_framework.middleware import MiddlewareManager
from kafka_framework.metrics import MetricsCollector
from kafka_framework.metrics.prometheus import PrometheusMetrics
from kafka_framework.middlewares import LoggingMiddleware, RetryMiddleware

from .handlers.user_handlers import UserHandlers
from .handlers.order_handlers import OrderHandlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

class MockDBClient:
    """Mock database client for demonstration purposes."""
    pass

class MockEmailService:
    """Mock email service for demonstration purposes."""
    pass

class MockPaymentService:
    """Mock payment service for demonstration purposes."""
    pass

class MockInventoryService:
    """Mock inventory service for demonstration purposes."""
    pass

def create_app() -> KafkaApp:
    """Create and configure the Kafka application."""
    # Initialize services
    db_client = MockDBClient()
    email_service = MockEmailService()
    payment_service = MockPaymentService()
    inventory_service = MockInventoryService()
    
    # Initialize metrics collector (Prometheus in this case)
    metrics = PrometheusMetrics(
        namespace="kafka_framework_example",
        port=9091  # Default Prometheus metrics port
    )
    
    # Create router and register handlers
    router = TopicRouter()
    
    # Initialize and register user handlers
    user_handlers = UserHandlers(db_client, email_service)
    router.register_handlers(user_handlers)
    
    # Initialize and register order handlers
    order_handlers = OrderHandlers(db_client, payment_service, inventory_service)
    router.register_handlers(order_handlers)
    
    # Set up middleware
    middleware_manager = MiddlewareManager()
    
    # Add logging middleware (logs before and after message processing)
    middleware_manager.add_middleware(LoggingMiddleware())
    
    # Add retry middleware (retries failed messages with exponential backoff)
    middleware_manager.add_middleware(
        RetryMiddleware(
            max_retries=3,
            initial_delay=1.0,
            max_delay=30.0,
            jitter=0.1,
            retry_exceptions=(Exception,)
        )
    )
    
    # Create the Kafka application
    app = KafkaApp(
        router=router,
        middleware_manager=middleware_manager,
        metrics=metrics,
        # These would typically come from environment variables
        kafka_config={
            "bootstrap_servers": "localhost:9092",
            "group_id": "example-consumer-group",
            "auto_offset_reset": "earliest",
            "enable_auto_commit": False,
        },
        consumer_config={
            "max_poll_records": 100,
            "session_timeout_ms": 30000,
            "heartbeat_interval_ms": 10000,
        },
        producer_config={
            "acks": "all",
            "retries": 3,
            "compression_type": "gzip",
        }
    )
    
    # Register startup and shutdown event handlers
    @app.on_startup
    async def startup() -> None:
        """Initialize resources on application startup."""
        logger.info("Starting Kafka consumer...")
        await metrics.start_server()
        logger.info("Application startup complete")
    
    @app.on_shutdown
    async def shutdown() -> None:
        """Clean up resources on application shutdown."""
        logger.info("Shutting down Kafka consumer...")
        await metrics.stop_server()
        logger.info("Application shutdown complete")
    
    return app

async def main() -> None:
    """Run the Kafka consumer application."""
    app = create_app()
    
    # Handle graceful shutdown
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()
    
    def signal_handler() -> None:
        logger.info("Received shutdown signal, stopping application...")
        stop_event.set()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        # Start the Kafka consumer
        await app.run()
        
        # Keep the application running until stop event is set
        await stop_event.wait()
        
    except asyncio.CancelledError:
        logger.info("Application was cancelled")
    except Exception as e:
        logger.exception("Application error")
        raise
    finally:
        # Ensure proper shutdown
        await app.stop()
        logger.info("Application stopped")

if __name__ == "__main__":
    asyncio.run(main())
