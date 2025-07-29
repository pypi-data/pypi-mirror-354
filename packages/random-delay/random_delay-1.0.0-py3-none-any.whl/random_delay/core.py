"""
Core delay classes and strategies
"""

import asyncio
import math
import random
import threading
import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional, Union

from .exceptions import DelayInterruptedError, InvalidDelayConfigError


class RandomDelay(ABC):
    """
    Abstract base class for random delay strategies
    """

    def __init__(
        self, min_delay: float = 0.0, max_delay: float = 1.0, seed: Optional[int] = None
    ):
        """
        Initialize random delay

        Args:
            min_delay: Minimum delay in seconds
            max_delay: Maximum delay in seconds
            seed: Random seed for reproducible delays
        """
        if min_delay < 0:
            raise InvalidDelayConfigError("min_delay cannot be negative")
        if max_delay < min_delay:
            raise InvalidDelayConfigError("max_delay must be >= min_delay")

        self.min_delay = min_delay
        self.max_delay = max_delay
        self._random = random.Random(seed)
        self._interrupted = threading.Event()

    @abstractmethod
    def _calculate_delay(self) -> float:
        """Calculate the next delay duration"""
        pass

    def delay(self) -> float:
        """
        Perform a synchronous delay

        Returns:
            Actual delay duration that was executed
        """
        delay_duration = self._calculate_delay()
        delay_duration = max(self.min_delay, min(self.max_delay, delay_duration))

        if delay_duration <= 0:
            return 0.0

        # Check for interruption periodically during long delays
        if delay_duration > 0.1:
            end_time = time.time() + delay_duration
            while time.time() < end_time:
                if self._interrupted.is_set():
                    raise DelayInterruptedError("Delay was interrupted")
                remaining = end_time - time.time()
                sleep_time = min(0.1, remaining)
                if sleep_time > 0:
                    time.sleep(sleep_time)
        else:
            time.sleep(delay_duration)

        return delay_duration

    async def async_delay(self) -> float:
        """
        Perform an asynchronous delay

        Returns:
            Actual delay duration that was executed
        """
        delay_duration = self._calculate_delay()
        delay_duration = max(self.min_delay, min(self.max_delay, delay_duration))

        if delay_duration <= 0:
            return 0.0

        # Use asyncio.sleep for non-blocking delays
        await asyncio.sleep(delay_duration)
        return delay_duration

    def interrupt(self):
        """Interrupt any ongoing synchronous delays"""
        self._interrupted.set()

    def reset_interrupt(self):
        """Reset the interrupt flag"""
        self._interrupted.clear()

    def get_next_delay(self) -> float:
        """Get the next delay duration without executing it"""
        delay_duration = self._calculate_delay()
        return max(self.min_delay, min(self.max_delay, delay_duration))


class UniformDelay(RandomDelay):
    """
    Uniform random delay between min_delay and max_delay
    """

    def _calculate_delay(self) -> float:
        return self._random.uniform(self.min_delay, self.max_delay)


class ExponentialDelay(RandomDelay):
    """
    Exponential distribution delay
    """

    def __init__(self, lambd: float = 1.0, **kwargs):
        """
        Initialize exponential delay

        Args:
            lambd: Lambda parameter for exponential distribution (rate parameter)
            **kwargs: Additional arguments passed to RandomDelay
        """
        super().__init__(**kwargs)
        if lambd <= 0:
            raise InvalidDelayConfigError("lambd must be positive")
        self.lambd = lambd

    def _calculate_delay(self) -> float:
        return self._random.expovariate(self.lambd)


class NormalDelay(RandomDelay):
    """
    Normal (Gaussian) distribution delay
    """

    def __init__(self, mu: float = 0.5, sigma: float = 0.1, **kwargs):
        """
        Initialize normal delay

        Args:
            mu: Mean of the normal distribution
            sigma: Standard deviation of the normal distribution
            **kwargs: Additional arguments passed to RandomDelay
        """
        super().__init__(**kwargs)
        if sigma <= 0:
            raise InvalidDelayConfigError("sigma must be positive")
        self.mu = mu
        self.sigma = sigma

    def _calculate_delay(self) -> float:
        return self._random.normalvariate(self.mu, self.sigma)


class ExponentialBackoffDelay(RandomDelay):
    """
    Exponential backoff delay with jitter
    """

    def __init__(
        self,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        multiplier: float = 2.0,
        jitter: bool = True,
        **kwargs
    ):
        """
        Initialize exponential backoff delay

        Args:
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            multiplier: Backoff multiplier
            jitter: Whether to add random jitter
            **kwargs: Additional arguments passed to RandomDelay
        """
        super().__init__(min_delay=0, max_delay=max_delay, **kwargs)
        if base_delay <= 0:
            raise InvalidDelayConfigError("base_delay must be positive")
        if multiplier <= 1:
            raise InvalidDelayConfigError("multiplier must be > 1")

        self.base_delay = base_delay
        self.multiplier = multiplier
        self.jitter = jitter
        self.attempt = 0

    def _calculate_delay(self) -> float:
        # Calculate exponential backoff
        delay = self.base_delay * (self.multiplier**self.attempt)

        # Add jitter if enabled
        if self.jitter:
            # Full jitter: random between 0 and calculated delay
            delay = self._random.uniform(0, delay)

        self.attempt += 1
        return delay

    def reset(self):
        """Reset the attempt counter"""
        self.attempt = 0


class CustomDelay(RandomDelay):
    """
    Custom delay using a user-provided function
    """

    def __init__(self, delay_func: Callable[[], float], **kwargs):
        """
        Initialize custom delay

        Args:
            delay_func: Function that returns delay duration
            **kwargs: Additional arguments passed to RandomDelay
        """
        super().__init__(**kwargs)
        if not callable(delay_func):
            raise InvalidDelayConfigError("delay_func must be callable")
        self.delay_func = delay_func

    def _calculate_delay(self) -> float:
        return self.delay_func()
