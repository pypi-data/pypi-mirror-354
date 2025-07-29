"""
Command-line interface for random-delay
"""

try:
    import click
    from rich import print as rprint
    from rich.console import Console
    from rich.progress import Progress
    from rich.table import Table

    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False
    click = None
    Console = None

import asyncio
import json
import time
from typing import Optional

from . import __version__
from .core import (CustomDelay, ExponentialBackoffDelay, ExponentialDelay,
                   NormalDelay, UniformDelay)
from .utils import benchmark_delay_strategy, delay_distribution_analysis

if not CLI_AVAILABLE:

    def main():
        print(
            "CLI dependencies not installed. Install with: pip install 'random-delay[cli]'"
        )
        return

else:
    console = Console()

    @click.group()
    @click.version_option(version=__version__)
    def cli():
        """Random Delay - Create random delays for rate limiting, jitter, or testing"""
        pass

    @cli.command()
    @click.option(
        "--strategy",
        "-s",
        type=click.Choice(["uniform", "exponential", "normal", "backoff"]),
        default="uniform",
        help="Delay strategy to use",
    )
    @click.option(
        "--min-delay", "-min", type=float, default=0.1, help="Minimum delay in seconds"
    )
    @click.option(
        "--max-delay", "-max", type=float, default=1.0, help="Maximum delay in seconds"
    )
    @click.option(
        "--count", "-c", type=int, default=10, help="Number of delays to execute"
    )
    @click.option(
        "--lambda",
        "lambd",
        type=float,
        default=1.0,
        help="Lambda for exponential distribution",
    )
    @click.option("--mu", type=float, default=0.5, help="Mean for normal distribution")
    @click.option(
        "--sigma", type=float, default=0.1, help="Std dev for normal distribution"
    )
    @click.option(
        "--base-delay",
        type=float,
        default=1.0,
        help="Base delay for exponential backoff",
    )
    @click.option(
        "--multiplier",
        type=float,
        default=2.0,
        help="Multiplier for exponential backoff",
    )
    @click.option(
        "--no-jitter", is_flag=True, help="Disable jitter for exponential backoff"
    )
    @click.option("--async-mode", is_flag=True, help="Use async delays")
    @click.option("--quiet", "-q", is_flag=True, help="Quiet output")
    def run(
        strategy,
        min_delay,
        max_delay,
        count,
        lambd,
        mu,
        sigma,
        base_delay,
        multiplier,
        no_jitter,
        async_mode,
        quiet,
    ):
        """Run delays with specified strategy"""

        # Create delay strategy
        if strategy == "uniform":
            delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)
        elif strategy == "exponential":
            delay_strategy = ExponentialDelay(
                lambd=lambd, min_delay=min_delay, max_delay=max_delay
            )
        elif strategy == "normal":
            delay_strategy = NormalDelay(
                mu=mu, sigma=sigma, min_delay=min_delay, max_delay=max_delay
            )
        elif strategy == "backoff":
            delay_strategy = ExponentialBackoffDelay(
                base_delay=base_delay,
                max_delay=max_delay,
                multiplier=multiplier,
                jitter=not no_jitter,
            )

        if not quiet:
            console.print(f"[bold green]Running {count} {strategy} delays[/bold green]")
            console.print(f"Strategy: {delay_strategy.__class__.__name__}")
            console.print(f"Range: {min_delay:.3f}s - {max_delay:.3f}s")
            console.print(f"Mode: {'Async' if async_mode else 'Sync'}")
            console.print()

        # Execute delays
        total_time = 0
        delays = []

        async def run_async_delays():
            nonlocal total_time, delays
            start_time = time.time()

            with Progress() as progress:
                task = progress.add_task("[green]Executing delays...", total=count)

                for i in range(count):
                    delay_start = time.time()
                    actual_delay = await delay_strategy.async_delay()
                    delay_end = time.time()

                    delays.append(actual_delay)

                    if not quiet:
                        progress.update(
                            task,
                            advance=1,
                            description=f"[green]Delay {i+1}/{count}: {actual_delay:.3f}s",
                        )

            total_time = time.time() - start_time

        def run_sync_delays():
            nonlocal total_time, delays
            start_time = time.time()

            with Progress() as progress:
                task = progress.add_task("[green]Executing delays...", total=count)

                for i in range(count):
                    delay_start = time.time()
                    actual_delay = delay_strategy.delay()
                    delay_end = time.time()

                    delays.append(actual_delay)

                    if not quiet:
                        progress.update(
                            task,
                            advance=1,
                            description=f"[green]Delay {i+1}/{count}: {actual_delay:.3f}s",
                        )

            total_time = time.time() - start_time

        # Execute based on mode
        if async_mode:
            asyncio.run(run_async_delays())
        else:
            run_sync_delays()

        # Display results
        if not quiet:
            console.print()
            console.print("[bold blue]Results:[/bold blue]")
            console.print(f"Total time: {total_time:.3f}s")
            console.print(f"Average delay: {sum(delays)/len(delays):.3f}s")
            console.print(f"Min delay: {min(delays):.3f}s")
            console.print(f"Max delay: {max(delays):.3f}s")

    @cli.command()
    @click.option(
        "--strategy",
        "-s",
        type=click.Choice(["uniform", "exponential", "normal", "backoff"]),
        default="uniform",
        help="Delay strategy to benchmark",
    )
    @click.option(
        "--iterations", "-i", type=int, default=100, help="Number of iterations"
    )
    @click.option("--min-delay", type=float, default=0.01, help="Minimum delay")
    @click.option("--max-delay", type=float, default=0.1, help="Maximum delay")
    @click.option("--async-mode", is_flag=True, help="Benchmark async mode")
    @click.option("--output", "-o", help="Output file for results (JSON)")
    def benchmark(strategy, iterations, min_delay, max_delay, async_mode, output):
        """Benchmark delay strategies"""

        # Create delay strategy
        if strategy == "uniform":
            delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)
        elif strategy == "exponential":
            delay_strategy = ExponentialDelay(
                lambd=10, min_delay=min_delay, max_delay=max_delay
            )
        elif strategy == "normal":
            delay_strategy = NormalDelay(
                mu=(min_delay + max_delay) / 2,
                sigma=0.01,
                min_delay=min_delay,
                max_delay=max_delay,
            )
        elif strategy == "backoff":
            delay_strategy = ExponentialBackoffDelay(
                base_delay=min_delay, max_delay=max_delay
            )

        console.print(f"[bold green]Benchmarking {strategy} strategy[/bold green]")
        console.print(f"Iterations: {iterations}")
        console.print(f"Mode: {'Async' if async_mode else 'Sync'}")

        # Run benchmark
        with console.status("[bold green]Running benchmark..."):
            results = benchmark_delay_strategy(delay_strategy, iterations, async_mode)

        # Display results
        table = Table(title="Benchmark Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Strategy", strategy.capitalize())
        table.add_row("Iterations", str(iterations))
        table.add_row("Mode", "Async" if async_mode else "Sync")
        table.add_row("", "")  # Separator

        table.add_row("Min Delay", f"{results['delays']['min']:.6f}s")
        table.add_row("Max Delay", f"{results['delays']['max']:.6f}s")
        table.add_row("Mean Delay", f"{results['delays']['mean']:.6f}s")
        table.add_row("Median Delay", f"{results['delays']['median']:.6f}s")
        table.add_row("Std Dev", f"{results['delays']['stdev']:.6f}s")
        table.add_row("", "")  # Separator

        table.add_row("Mean Overhead", f"{results['overhead']['mean']*1000:.3f}ms")
        table.add_row("Max Overhead", f"{results['overhead']['max']*1000:.3f}ms")

        console.print(table)

        # Save to file if requested
        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2)
            console.print(f"\n[green]Results saved to {output}[/green]")

    @cli.command()
    @click.option(
        "--strategy",
        "-s",
        type=click.Choice(["uniform", "exponential", "normal"]),
        default="uniform",
        help="Delay strategy to analyze",
    )
    @click.option(
        "--samples", type=int, default=1000, help="Number of samples to generate"
    )
    @click.option("--min-delay", type=float, default=0.1, help="Minimum delay")
    @click.option("--max-delay", type=float, default=1.0, help="Maximum delay")
    @click.option("--output", "-o", help="Output file for analysis (JSON)")
    def analyze(strategy, samples, min_delay, max_delay, output):
        """Analyze delay distribution"""

        # Create delay strategy
        if strategy == "uniform":
            delay_strategy = UniformDelay(min_delay=min_delay, max_delay=max_delay)
        elif strategy == "exponential":
            delay_strategy = ExponentialDelay(
                lambd=2, min_delay=min_delay, max_delay=max_delay
            )
        elif strategy == "normal":
            delay_strategy = NormalDelay(
                mu=(min_delay + max_delay) / 2,
                sigma=0.1,
                min_delay=min_delay,
                max_delay=max_delay,
            )

        console.print(f"[bold green]Analyzing {strategy} distribution[/bold green]")
        console.print(f"Samples: {samples}")

        # Run analysis
        with console.status("[bold green]Generating samples..."):
            results = delay_distribution_analysis(delay_strategy, samples)

        # Display results
        table = Table(title="Distribution Analysis")
        table.add_column("Statistic", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Samples", str(results["samples"]))
        table.add_row("Min", f"{results['min']:.6f}s")
        table.add_row("Max", f"{results['max']:.6f}s")
        table.add_row("Mean", f"{results['mean']:.6f}s")
        table.add_row("Median", f"{results['median']:.6f}s")
        table.add_row("Std Dev", f"{results['stdev']:.6f}s")
        table.add_row("Variance", f"{results['variance']:.6f}")

        console.print(table)

        # Percentiles table
        perc_table = Table(title="Percentiles")
        perc_table.add_column("Percentile", style="cyan")
        perc_table.add_column("Value", style="green")

        for p, value in results["percentiles"].items():
            perc_table.add_row(p.upper(), f"{value:.6f}s")

        console.print(perc_table)

        # Save to file if requested
        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2)
            console.print(f"\n[green]Analysis saved to {output}[/green]")

    def main():
        """Main CLI entry point"""
        cli()


if __name__ == "__main__":
    main()
