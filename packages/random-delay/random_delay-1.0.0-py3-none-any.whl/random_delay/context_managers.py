"""
Context managers for delay operations
"""

import asyncio
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Optional

from .core import RandomDelay, UniformDelay


class DelayContext:
    """
    Synchronous context manager for delays
    """

    def __init__(
        self,
        delay_strategy: Optional[RandomDelay] = None,
        min_delay: float = 0.1,
        max_delay: float = 1.0,
        before: bool = True,
        after: bool = False,
    ):
        """
        Initialize delay context

        Args:
            delay_strategy: RandomDelay instance to use
            min_delay: Minimum delay if no strategy provided
            max_delay: Maximum delay if no strategy provided
            before: Add delay when entering context
            after: Add delay when exiting context
        """
        if delay_strategy is None:
            delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)

        self.delay_strategy = delay_strategy
        self.before = before
        self.after = after
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()

        if self.before:
            self.delay_strategy.delay()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.after:
            self.delay_strategy.delay()

        self.end_time = time.time()

    @property
    def duration(self) -> Optional[float]:
        """Get the total duration of the context (including delays)"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class AsyncDelayContext:
    """
    Asynchronous context manager for delays
    """

    def __init__(
        self,
        delay_strategy: Optional[RandomDelay] = None,
        min_delay: float = 0.1,
        max_delay: float = 1.0,
        before: bool = True,
        after: bool = False,
    ):
        """
        Initialize async delay context

        Args:
            delay_strategy: RandomDelay instance to use
            min_delay: Minimum delay if no strategy provided
            max_delay: Maximum delay if no strategy provided
            before: Add delay when entering context
            after: Add delay when exiting context
        """
        if delay_strategy is None:
            delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)

        self.delay_strategy = delay_strategy
        self.before = before
        self.after = after
        self.start_time = None
        self.end_time = None

    async def __aenter__(self):
        self.start_time = time.time()

        if self.before:
            await self.delay_strategy.async_delay()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.after:
            await self.delay_strategy.async_delay()

        self.end_time = time.time()

    @property
    def duration(self) -> Optional[float]:
        """Get the total duration of the context (including delays)"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


# Convenience functions
@contextmanager
def delay_context(
    delay_strategy: Optional[RandomDelay] = None,
    min_delay: float = 0.1,
    max_delay: float = 1.0,
    before: bool = True,
    after: bool = False,
):
    """
    Convenience function for DelayContext
    """
    context = DelayContext(delay_strategy, min_delay, max_delay, before, after)
    with context:
        yield context


@asynccontextmanager
async def async_delay_context(
    delay_strategy: Optional[RandomDelay] = None,
    min_delay: float = 0.1,
    max_delay: float = 1.0,
    before: bool = True,
    after: bool = False,
):
    """
    Convenience function for AsyncDelayContext
    """
    context = AsyncDelayContext(delay_strategy, min_delay, max_delay, before, after)
    async with context:
        yield context
