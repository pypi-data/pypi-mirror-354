"""
Custom exceptions for random-delay package
"""


class RandomDelayError(Exception):
    """Base exception for random-delay package"""

    pass


class InvalidDelayConfigError(RandomDelayError):
    """Raised when delay configuration is invalid"""

    pass


class DelayTimeoutError(RandomDelayError):
    """Raised when delay operation times out"""

    pass


class DelayInterruptedError(RandomDelayError):
    """Raised when delay is interrupted"""

    pass
