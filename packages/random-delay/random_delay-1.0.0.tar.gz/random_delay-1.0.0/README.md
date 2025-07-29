# Random Delay

🎲 Create random delays for rate limiting, jitter, or testing.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/random-delay.svg)](https://badge.fury.io/py/random-delay)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Features

🚀 **Multiple Delay Strategies**
- Uniform random delays
- Exponential distribution delays
- Normal (Gaussian) distribution delays
- Exponential backoff with jitter
- Custom delay functions

⚡ **Async/Await Support**
- Full support for both sync and async operations
- Non-blocking delays with `asyncio`

🎯 **Easy Integration**
- Decorators for functions
- Context managers
- Direct delay calls

🔄 **Retry Mechanisms**
- Automatic retries with configurable delays
- Exception handling
- Callback support

📊 **Analysis Tools**
- Benchmark delay strategies
- Distribution analysis
- Performance metrics

## Installation

```bash
pip install random-delay
```

For CLI support:
```bash
pip install random-delay[cli]
```

For development:
```bash
pip install random-delay[dev]
```

## Quick Start

### Basic Usage

```python
import random_delay

# Create a uniform delay between 0.1 and 0.5 seconds
delay = random_delay.UniformDelay(min_delay=0.1, max_delay=0.5)

# Synchronous delay
delay.delay()

# Asynchronous delay
await delay.async_delay()
```

### Using Decorators

```python
from random_delay import delay, async_delay

# Add delay before function execution
@delay(min_delay=0.1, max_delay=0.5)
def api_call():
    return "API response"

# Async version
@async_delay(min_delay=0.1, max_delay=0.5)
async def async_api_call():
    return "Async API response"
```

### Retry with Exponential Backoff

```python
from random_delay import retry_with_delay, ExponentialBackoffDelay
import requests

@retry_with_delay(
    max_retries=3,
    delay_strategy=ExponentialBackoffDelay(base_delay=1.0, max_delay=60.0)
)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### Context Managers

```python
from random_delay import DelayContext, UniformDelay

delay_strategy = UniformDelay(0.1, 0.5)

# Add delay when entering context
with DelayContext(delay_strategy, before=True):
    print("This executes after a random delay")

# Async version
async with AsyncDelayContext(delay_strategy, before=True, after=True):
    print("Delays before and after this block")
```

## Delay Strategies

### Uniform Delay
Random delay uniformly distributed between min and max values.

```python
from random_delay import UniformDelay

delay = UniformDelay(min_delay=0.1, max_delay=1.0)
```

### Exponential Delay
Delay following exponential distribution (good for simulating real-world wait times).

```python
from random_delay import ExponentialDelay

delay = ExponentialDelay(lambd=1.0, max_delay=5.0)
```

### Normal Delay
Delay following normal (Gaussian) distribution.

```python
from random_delay import NormalDelay

delay = NormalDelay(mu=0.5, sigma=0.1, min_delay=0.1, max_delay=1.0)
```

### Exponential Backoff
Delay that increases exponentially with each attempt (perfect for retries).

```python
from random_delay import ExponentialBackoffDelay

delay = ExponentialBackoffDelay(
    base_delay=1.0,
    max_delay=60.0,
    multiplier=2.0,
    jitter=True
)

# Use for retries
for attempt in range(3):
    try:
        risky_operation()
        break
    except Exception:
        delay.delay()  # Wait longer each time
```

### Custom Delay
Use your own function to generate delays.

```python
from random_delay import CustomDelay
import random

def my_delay_func():
    return random.triangular(0.1, 1.0, 0.3)

delay = CustomDelay(my_delay_func)
```

## Common Use Cases

### Rate Limiting
```python
from random_delay.utils import create_rate_limiter

# Limit to 10 requests per second with jitter
rate_limiter = create_rate_limiter(requests_per_second=10, jitter=True)

for i in range(100):
    rate_limiter.delay()
    make_api_request()
```

### Preventing Thundering Herd
```python
from random_delay import UniformDelay

# Add jitter to prevent all clients hitting at the same time
jitter = UniformDelay(0.0, 2.0)

def scheduled_task():
    jitter.delay()  # Random delay before execution
    perform_task()
```

### Testing Network Conditions
```python
from random_delay.utils import simulate_network_latency
from random_delay import CustomDelay

# Simulate network with 10-100ms latency and 1% packet loss
latency_sim = simulate_network_latency(
    min_latency=0.01,
    max_latency=0.1,
    packet_loss_rate=0.01
)

network_delay = CustomDelay(latency_sim)

def test_with_network_simulation():
    network_delay.delay()
    # Your network-dependent code here
```

### Graceful Degradation
```python
from random_delay import ExponentialBackoffDelay, async_retry_with_delay

backoff = ExponentialBackoffDelay(base_delay=0.1, max_delay=30.0)

@async_retry_with_delay(
    max_retries=5,
    delay_strategy=backoff,
    exceptions=(ConnectionError, TimeoutError)
)
async def robust_api_call():
    # This will retry with exponential backoff on connection errors
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/data') as response:
            return await response.json()
```

## Command Line Interface

The package includes a CLI for testing and analysis:

```bash
# Run 10 uniform delays between 0.1 and 0.5 seconds
random-delay run --strategy uniform --min-delay 0.1 --max-delay 0.5 --count 10

# Benchmark exponential delays
random-delay benchmark --strategy exponential --iterations 1000

# Analyze delay distribution
random-delay analyze --strategy normal --samples 10000 --output analysis.json
```

## Advanced Features

### Interrupting Delays
```python
import threading
from random_delay import UniformDelay

delay = UniformDelay(5.0, 10.0)

# In another thread
def interrupt_after_timeout():
    time.sleep(2.0)
    delay.interrupt()

threading.Thread(target=interrupt_after_timeout).start()

try:
    delay.delay()  # Will be interrupted after 2 seconds
except DelayInterruptedError:
    print("Delay was interrupted")
```

### Benchmarking Strategies
```python
from random_delay.utils import benchmark_delay_strategy
from random_delay import UniformDelay

delay = UniformDelay(0.01, 0.1)
results = benchmark_delay_strategy(delay, iterations=1000, async_mode=True)

print(f"Average delay: {results['delays']['mean']:.4f}s")
print(f"Overhead: {results['overhead']['mean']*1000:.2f}ms")
```

### Distribution Analysis
```python
from random_delay.utils import delay_distribution_analysis
from random_delay import NormalDelay

delay = NormalDelay(mu=0.5, sigma=0.1)
analysis = delay_distribution_analysis(delay, samples=10000)

print(f"Mean: {analysis['mean']:.4f}s")
print(f"Std Dev: {analysis['stdev']:.4f}s")
print(f"95th percentile: {analysis['percentiles']['p95']:.4f}s")
```

## Performance Considerations

- **Async delays** are more efficient for I/O-bound applications
- **Thread overhead** is minimal for short delays (< 1ms)
- **Memory usage** is constant regardless of delay duration
- **Jitter** adds ~10-20μs overhead but prevents thundering herd

## Best Practices

### For Rate Limiting
```python
# ✅ Good: Use jitter to prevent thundering herd
rate_limiter = create_rate_limiter(10, jitter=True)

# ❌ Avoid: Fixed delays can cause synchronized requests
fixed_delay = CustomDelay(lambda: 0.1)
```

### For Retries
```python
# ✅ Good: Exponential backoff with jitter
backoff = ExponentialBackoffDelay(base_delay=1.0, jitter=True)

# ❌ Avoid: Linear backoff can be too aggressive
linear_delay = CustomDelay(lambda: attempt * 1.0)
```

### For Testing
```python
# ✅ Good: Use realistic distributions
realistic_delay = NormalDelay(mu=0.1, sigma=0.02)

# ❌ Avoid: Unrealistic uniform delays
unrealistic_delay = UniformDelay(0.001, 10.0)
```

## API Reference

### Core Classes

- **`RandomDelay`** - Abstract base class for all delay strategies
- **`UniformDelay`** - Uniform random delays
- **`ExponentialDelay`** - Exponential distribution delays
- **`NormalDelay`** - Normal distribution delays
- **`ExponentialBackoffDelay`** - Exponential backoff with jitter
- **`CustomDelay`** - User-defined delay functions

### Decorators

- **`@delay`** - Add delays to synchronous functions
- **`@async_delay`** - Add delays to asynchronous functions
- **`@retry_with_delay`** - Retry with delay on exception
- **`@async_retry_with_delay`** - Async retry with delay

### Context Managers

- **`DelayContext`** - Synchronous delay context manager
- **`AsyncDelayContext`** - Asynchronous delay context manager

### Utilities

- **`create_rate_limiter`** - Create rate limiting delays
- **`create_exponential_backoff`** - Create exponential backoff
- **`simulate_network_latency`** - Simulate network conditions
- **`benchmark_delay_strategy`** - Benchmark performance
- **`delay_distribution_analysis`** - Analyze distributions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone https://github.com/yourusername/random-delay.git
cd random-delay
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=random_delay  # With coverage
```

### Code Formatting

```bash
black random_delay/
isort random_delay/
flake8 random_delay/
```

---

## Why Random Delays?

Random delays are essential for building robust distributed systems:

- **Prevents thundering herd** - Avoids all clients hitting resources simultaneously
- **Improves system stability** - Spreads load over time
- **Better user experience** - Graceful degradation under load
- **Testing realism** - Simulates real-world network conditions
- **Rate limiting** - Respects API limits and prevents abuse

Perfect for microservices, API clients, testing frameworks, and any system that needs intelligent delay strategies!