"""
Benchmarks Abstraction Module

This module provides a generic interface for defining and running benchmarks
against System Under Test implementations.

Example:
    >>> from benchmarks import BenchmarkRunner, register_benchmark, create_benchmark
    >>>
    >>> class MyBenchmark(BenchmarkRunner):
    ...     name = "my_bench"
    ...     def run(self, sut, config): ...
    ...     def parse_results(self, output): ...
    ...
    >>> register_benchmark("my_bench", MyBenchmark)
    >>> bench = create_benchmark("my_bench")
"""

from .base import BenchmarkRunner, BenchmarkResult, BenchmarkStatus
from .registry import (
    register_benchmark,
    unregister_benchmark,
    get_available_benchmarks,
    get_benchmark_class,
    is_benchmark_registered,
    create_benchmark,
    list_benchmarks_info,
    get_benchmarks_for_sut,
)

__all__ = [
    # Base classes
    "BenchmarkRunner",
    "BenchmarkResult",
    "BenchmarkStatus",
    # Registry functions
    "register_benchmark",
    "unregister_benchmark",
    "get_available_benchmarks",
    "get_benchmark_class",
    "is_benchmark_registered",
    "create_benchmark",
    "list_benchmarks_info",
    "get_benchmarks_for_sut",
]
