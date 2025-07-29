"""
Random Delay - Create random delays for rate limiting, jitter, or testing

This package provides various strategies for creating random delays:
- Uniform distribution delays
- Exponential distribution delays
- Normal (Gaussian) distribution delays
- Exponential backoff with jitter
- Custom distribution delays

Supports both synchronous and asynchronous operations.
"""

__version__ = "1.0.0"
__author__ = "Abderrahim GHAZALI"
__email__ = "ghazali.abderrahim1@gmail.com"

from .context_managers import AsyncDelayContext, DelayContext
from .core import (CustomDelay, ExponentialBackoffDelay, ExponentialDelay,
                   NormalDelay, RandomDelay, UniformDelay)
from .decorators import (async_delay, async_retry_with_delay, delay,
                         retry_with_delay)
from .exceptions import (DelayInterruptedError, DelayTimeoutError,
                         InvalidDelayConfigError, RandomDelayError)

__all__ = [
    # Core classes
    "RandomDelay",
    "UniformDelay",
    "ExponentialDelay",
    "NormalDelay",
    "ExponentialBackoffDelay",
    "CustomDelay",
    # Decorators
    "delay",
    "async_delay",
    "retry_with_delay",
    "async_retry_with_delay",
    # Context managers
    "DelayContext",
    "AsyncDelayContext",
    # Exceptions
    "RandomDelayError",
    "InvalidDelayConfigError",
    "DelayTimeoutError",
    "DelayInterruptedError",
]
