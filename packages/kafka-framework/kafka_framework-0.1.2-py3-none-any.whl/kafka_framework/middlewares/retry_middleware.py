import asyncio
import random
import logging
from typing import Any, Callable, Type, TypeVar
from kafka_framework.types import MessageContext
from .base import BaseMiddleware

logger = logging.getLogger(__name__)
T = TypeVar("T")


class RetryMiddleware(BaseMiddleware):
    """Middleware that retries message processing on transient errors."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 0.1,
        max_delay: float = 5.0,
        backoff_factor: float = 2.0,
        jitter: float = 0.1,
        retry_exceptions: tuple[Type[Exception], ...] = (Exception,),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.retry_exceptions = retry_exceptions

    async def __call__(self, ctx: MessageContext, call_next: Callable) -> Any:
        """Execute the next middleware with retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    delay = self._get_retry_delay(attempt)
                    logger.warning(
                        f"Retry attempt {attempt}/{self.max_retries} after {delay:.2f}s "
                        f"for message at offset {ctx.offset} in partition {ctx.partition}"
                    )
                    await asyncio.sleep(delay)

                return await call_next(ctx)

            except self.retry_exceptions as e:
                last_exception = e
                if attempt == self.max_retries:
                    logger.error(
                        f"Max retries ({self.max_retries}) exceeded for message at "
                        f"offset {ctx.offset} in partition {ctx.partition}",
                        exc_info=True,
                    )
                    raise

        # This should never be reached due to the raise in the except block
        raise last_exception  # type: ignore

    def _get_retry_delay(self, attempt: int) -> float:
        """Calculate the delay for a retry attempt with exponential backoff and jitter."""
        delay = min(
            self.initial_delay * (self.backoff_factor ** (attempt - 1)), self.max_delay
        )
        jitter_amount = delay * self.jitter * (2 * random.random() - 1)
        return max(0, delay + jitter_amount)
