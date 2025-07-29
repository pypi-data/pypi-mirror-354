import logging
from typing import Any, Callable
from kafka_framework.types import MessageContext
from .base import BaseMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware that logs message processing details."""

    def __init__(self, log_level: int = logging.INFO, **kwargs):
        super().__init__(**kwargs)
        self.log_level = log_level

    async def __call__(self, ctx: MessageContext, call_next: Callable) -> Any:
        """Log message processing details before and after handling."""
        logger.log(
            self.log_level,
            f"Processing message from topic={ctx.topic} "
            f"partition={ctx.partition} offset={ctx.offset}",
        )

        try:
            result = await call_next(ctx)
            logger.log(
                self.log_level,
                f"Successfully processed message from topic={ctx.topic} "
                f"partition={ctx.partition} offset={ctx.offset}",
            )
            return result

        except Exception as e:
            logger.error(
                f"Error processing message from topic={ctx.topic} "
                f"partition={ctx.partition} offset={ctx.offset}: {str(e)}",
                exc_info=True,
            )
            raise
