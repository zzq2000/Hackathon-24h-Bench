"""Metrics module for LongAgentBench.

Parses agent iteration logs, extracts key metrics, correlates with benchmark
results, and produces JSON + CLI summary output.
"""

from metrics.models import IterationMetrics, BenchmarkSnapshot, RunMetrics
from metrics.aggregator import aggregate
from metrics.benchmark_linker import load_benchmarks
from metrics.report import to_json, print_summary

__all__ = [
    "IterationMetrics",
    "BenchmarkSnapshot",
    "RunMetrics",
    "aggregate",
    "load_benchmarks",
    "to_json",
    "print_summary",
]
