import asyncio
import logging
from typing import Any, Callable, List, Optional, TypeVar

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from .context import MessageContext
from .exceptions import KafkaFrameworkException
from .middleware import MiddlewareManager
from .router import TopicRouter

T = TypeVar('T')

logger = logging.getLogger(__name__)

class KafkaApp:
    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        group_id: Optional[str] = None,
        enable_auto_commit: bool = True,
        auto_offset_reset: str = "earliest",
    ):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.enable_auto_commit = enable_auto_commit
        self.auto_offset_reset = auto_offset_reset
        
        self._router = TopicRouter()
        self._middleware = MiddlewareManager()
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._producer: Optional[AIOKafkaProducer] = None
        self._startup_handlers: List[Callable] = []
        self._shutdown_handlers: List[Callable] = []
        self._running: bool = False
        
    async def startup(self):
        """Initialize and start Kafka consumer and producer"""
        if self._running:
            raise KafkaFrameworkException("Application is already running")
            
        # Initialize Kafka consumer
        self._consumer = AIOKafkaConsumer(
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=self.enable_auto_commit,
            auto_offset_reset=self.auto_offset_reset,
        )
        
        # Initialize Kafka producer
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        
        await self._consumer.start()
        await self._producer.start()
        
        # Run startup handlers
        for handler in self._startup_handlers:
            await handler()
            
        self._running = True
        logger.info("Kafka application started successfully")
        
    async def shutdown(self):
        """Clean up resources and shutdown"""
        if not self._running:
            return
            
        # Run shutdown handlers
        for handler in self._shutdown_handlers:
            await handler()
            
        # Stop consumer and producer
        if self._consumer:
            await self._consumer.stop()
        if self._producer:
            await self._producer.stop()
            
        self._running = False
        logger.info("Kafka application shutdown successfully")
        
    def on_startup(self, handler: Callable):
        """Register a startup handler"""
        self._startup_handlers.append(handler)
        return handler
        
    def on_shutdown(self, handler: Callable):
        """Register a shutdown handler"""
        self._shutdown_handlers.append(handler)
        return handler
        
    async def run(self):
        """Start the main consumption loop"""
        await self.startup()
        
        try:
            # Subscribe to all registered topics
            topics = self._router.get_all_topics()
            await self._consumer.subscribe(topics=topics)
            
            while True:
                # Get messages from Kafka
                msg = await self._consumer.getone()
                
                # Process the message
                await self._process_message(msg)
                
        except asyncio.CancelledError:
            logger.info("Consumption loop cancelled")
        except Exception as e:
            logger.error(f"Error in consumption loop: {str(e)}")
            raise
        finally:
            await self.shutdown()
            
    async def _process_message(self, msg):
        """Process a single Kafka message"""
        try:
            # Create message context
            ctx = MessageContext(
                topic=msg.topic,
                partition=msg.partition,
                offset=msg.offset,
                key=msg.key,
                value=msg.value,
                timestamp=msg.timestamp,
            )
            
            # Get handler for this topic
            handler = self._router.get_handler(msg.topic)
            if not handler:
                logger.warning(f"No handler registered for topic: {msg.topic}")
                return
                
            # Process through middleware and handler
            await self._middleware.process_message(ctx, handler)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
            
    async def publish(self, topic: str, value: Any, key: Optional[Any] = None):
        """Publish a message to a Kafka topic"""
        if not self._producer:
            raise KafkaFrameworkException("Producer is not initialized")
            
        await self._producer.send_and_wait(topic, value, key=key)
        
    def __del__(self):
        """Cleanup resources when app is garbage collected"""
        if self._running:
            asyncio.create_task(self.shutdown())
