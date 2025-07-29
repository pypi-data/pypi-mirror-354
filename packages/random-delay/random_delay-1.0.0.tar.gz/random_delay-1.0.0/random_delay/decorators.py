"""
Decorators for adding delays to functions
"""

import asyncio
import functools
import inspect
from typing import Any, Callable, Optional, Tuple, Type, Union

from .core import RandomDelay, UniformDelay
from .exceptions import RandomDelayError


def delay(
    delay_strategy: Optional[RandomDelay] = None,
    min_delay: float = 0.1,
    max_delay: float = 1.0,
    before: bool = True,
    after: bool = False,
) -> Callable:
    """
    Decorator to add random delay before and/or after function execution

    Args:
        delay_strategy: RandomDelay instance to use
        min_delay: Minimum delay if no strategy provided
        max_delay: Maximum delay if no strategy provided
        before: Add delay before function execution
        after: Add delay after function execution
    """
    if delay_strategy is None:
        delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Delay before execution
            if before:
                delay_strategy.delay()

            try:
                result = func(*args, **kwargs)
            finally:
                # Delay after execution (even if function raises)
                if after:
                    delay_strategy.delay()

            return result

        return wrapper

    return decorator


def async_delay(
    delay_strategy: Optional[RandomDelay] = None,
    min_delay: float = 0.1,
    max_delay: float = 1.0,
    before: bool = True,
    after: bool = False,
) -> Callable:
    """
    Async decorator to add random delay before and/or after function execution

    Args:
        delay_strategy: RandomDelay instance to use
        min_delay: Minimum delay if no strategy provided
        max_delay: Maximum delay if no strategy provided
        before: Add delay before function execution
        after: Add delay after function execution
    """
    if delay_strategy is None:
        delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Delay before execution
            if before:
                await delay_strategy.async_delay()

            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
            finally:
                # Delay after execution
                if after:
                    await delay_strategy.async_delay()

            return result

        return wrapper

    return decorator


def retry_with_delay(
    max_retries: int = 3,
    delay_strategy: Optional[RandomDelay] = None,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable] = None,
) -> Callable:
    """
    Decorator to retry function with delay on exception

    Args:
        max_retries: Maximum number of retry attempts
        delay_strategy: RandomDelay instance for retry delays
        exceptions: Exception types to catch for retry
        on_retry: Callback function called on each retry
    """
    if delay_strategy is None:
        from .core import ExponentialBackoffDelay

        delay_strategy = ExponentialBackoffDelay()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:  # Add delay before retry (not on first attempt)
                        delay_strategy.delay()

                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:  # Don't call on_retry for final failure
                        if on_retry:
                            on_retry(attempt + 1, e)
                    else:
                        # Final failure - re-raise the exception
                        raise last_exception

            # Should never reach here, but just in case
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def async_retry_with_delay(
    max_retries: int = 3,
    delay_strategy: Optional[RandomDelay] = None,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable] = None,
) -> Callable:
    """
    Async decorator to retry function with delay on exception

    Args:
        max_retries: Maximum number of retry attempts
        delay_strategy: RandomDelay instance for retry delays
        exceptions: Exception types to catch for retry
        on_retry: Callback function called on each retry
    """
    if delay_strategy is None:
        from .core import ExponentialBackoffDelay

        delay_strategy = ExponentialBackoffDelay()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:  # Add delay before retry
                        await delay_strategy.async_delay()

                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        if on_retry:
                            if asyncio.iscoroutinefunction(on_retry):
                                await on_retry(attempt + 1, e)
                            else:
                                on_retry(attempt + 1, e)
                    else:
                        raise last_exception

            if last_exception:
                raise last_exception

        return wrapper

    return decorator
