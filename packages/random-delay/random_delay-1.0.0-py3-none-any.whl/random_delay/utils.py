"""
Utility functions for random delays
"""

import asyncio
import statistics
import time
from typing import Any, Callable, Dict, List, Optional

from .core import RandomDelay


def benchmark_delay_strategy(
    delay_strategy: RandomDelay, iterations: int = 100, async_mode: bool = False
) -> Dict[str, Any]:
    """
    Benchmark a delay strategy

    Args:
        delay_strategy: The delay strategy to benchmark
        iterations: Number of iterations to run
        async_mode: Whether to use async delays

    Returns:
        Dictionary with benchmark results
    """
    delays = []
    durations = []

    if async_mode:

        async def run_async_benchmark():
            for _ in range(iterations):
                start_time = time.time()
                actual_delay = await delay_strategy.async_delay()
                end_time = time.time()

                delays.append(actual_delay)
                durations.append(end_time - start_time)

        # Run the async benchmark
        asyncio.run(run_async_benchmark())
    else:
        for _ in range(iterations):
            start_time = time.time()
            actual_delay = delay_strategy.delay()
            end_time = time.time()

            delays.append(actual_delay)
            durations.append(end_time - start_time)

    return {
        "iterations": iterations,
        "async_mode": async_mode,
        "delays": {
            "min": min(delays),
            "max": max(delays),
            "mean": statistics.mean(delays),
            "median": statistics.median(delays),
            "stdev": statistics.stdev(delays) if len(delays) > 1 else 0,
        },
        "actual_durations": {
            "min": min(durations),
            "max": max(durations),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
        },
        "overhead": {
            "mean": statistics.mean([d - delay for d, delay in zip(durations, delays)]),
            "max": max([d - delay for d, delay in zip(durations, delays)]),
        },
    }


def create_rate_limiter(requests_per_second: float, jitter: bool = True) -> RandomDelay:
    """
    Create a delay strategy for rate limiting

    Args:
        requests_per_second: Target requests per second
        jitter: Whether to add jitter to prevent thundering herd

    Returns:
        RandomDelay instance configured for rate limiting
    """
    if requests_per_second <= 0:
        raise ValueError("requests_per_second must be positive")

    base_delay = 1.0 / requests_per_second

    if jitter:
        from .core import UniformDelay

        # Add ±25% jitter
        min_delay = base_delay * 0.75
        max_delay = base_delay * 1.25
        return UniformDelay(min_delay=min_delay, max_delay=max_delay)
    else:
        from .core import CustomDelay

        return CustomDelay(lambda: base_delay)


def create_exponential_backoff(
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    multiplier: float = 2.0,
    jitter: bool = True,
) -> "ExponentialBackoffDelay":
    """
    Create an exponential backoff delay strategy

    Args:
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        multiplier: Backoff multiplier
        jitter: Whether to add jitter

    Returns:
        ExponentialBackoffDelay instance
    """
    from .core import ExponentialBackoffDelay

    return ExponentialBackoffDelay(
        base_delay=initial_delay,
        max_delay=max_delay,
        multiplier=multiplier,
        jitter=jitter,
    )


def simulate_network_latency(
    min_latency: float = 0.01, max_latency: float = 0.1, packet_loss_rate: float = 0.0
) -> Callable[[], Optional[float]]:
    """
    Create a function that simulates network latency

    Args:
        min_latency: Minimum latency in seconds
        max_latency: Maximum latency in seconds
        packet_loss_rate: Probability of packet loss (0.0 to 1.0)

    Returns:
        Function that returns delay duration or None for packet loss
    """
    import random

    def latency_func():
        # Simulate packet loss
        if random.random() < packet_loss_rate:
            return None  # Packet lost

        # Simulate network latency with some variation
        return random.uniform(min_latency, max_latency)

    return latency_func


def delay_distribution_analysis(
    delay_strategy: RandomDelay, samples: int = 1000
) -> Dict[str, Any]:
    """
    Analyze the distribution of delays from a strategy

    Args:
        delay_strategy: The delay strategy to analyze
        samples: Number of samples to generate

    Returns:
        Dictionary with distribution analysis
    """
    delays = [delay_strategy.get_next_delay() for _ in range(samples)]

    # Calculate percentiles
    sorted_delays = sorted(delays)

    def percentile(data, p):
        n = len(data)
        k = (n - 1) * p / 100
        f = int(k)
        c = k - f
        if f == n - 1:
            return data[f]
        else:
            return data[f] * (1 - c) + data[f + 1] * c

    return {
        "samples": samples,
        "min": min(delays),
        "max": max(delays),
        "mean": statistics.mean(delays),
        "median": statistics.median(delays),
        "mode": statistics.mode(delays) if len(set(delays)) < len(delays) else None,
        "stdev": statistics.stdev(delays) if len(delays) > 1 else 0,
        "variance": statistics.variance(delays) if len(delays) > 1 else 0,
        "percentiles": {
            "p10": percentile(sorted_delays, 10),
            "p25": percentile(sorted_delays, 25),
            "p50": percentile(sorted_delays, 50),
            "p75": percentile(sorted_delays, 75),
            "p90": percentile(sorted_delays, 90),
            "p95": percentile(sorted_delays, 95),
            "p99": percentile(sorted_delays, 99),
        },
    }
