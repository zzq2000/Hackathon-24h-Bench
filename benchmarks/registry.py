"""
Benchmark Registry Module

Provides registration and factory functions for Benchmark types.
"""

import logging
from typing import Dict, Type, Optional, Any, List

from .base import BenchmarkRunner

logger = logging.getLogger(__name__)


# Benchmark registry - stores all registered benchmark types
_BENCHMARK_REGISTRY: Dict[str, Type[BenchmarkRunner]] = {}


def _register_builtin_benchmarks() -> None:
    """Register built-in benchmark implementations."""
    try:
        from .implementations.sysbench import SysbenchRunner
        _BENCHMARK_REGISTRY["sysbench"] = SysbenchRunner
    except ImportError:
        logger.debug("Sysbench benchmark implementation not available")

    try:
        from .implementations.tpcc import TPCCRunner
        _BENCHMARK_REGISTRY["tpcc"] = TPCCRunner
    except ImportError:
        logger.debug("TPC-C benchmark implementation not available")

    try:
        from .implementations.tpch import TPCHRunner
        _BENCHMARK_REGISTRY["tpch"] = TPCHRunner
    except ImportError:
        logger.debug("TPC-H benchmark implementation not available")

    try:
        from .implementations.mq_bench import MessageQueueBenchRunner
        _BENCHMARK_REGISTRY["mq_bench"] = MessageQueueBenchRunner
    except ImportError:
        logger.debug("Message Queue benchmark implementation not available")

    try:
        from .implementations.http_bench import HttpBenchRunner
        _BENCHMARK_REGISTRY["http_bench"] = HttpBenchRunner
    except ImportError:
        logger.debug("HTTP benchmark implementation not available")

    try:
        from .implementations.redis_bench import RedisBenchRunner
        _BENCHMARK_REGISTRY["redis_bench"] = RedisBenchRunner
    except ImportError:
        logger.debug("Redis benchmark implementation not available")


def register_benchmark(name: str, benchmark_class: Type[BenchmarkRunner]) -> None:
    """
    Register a new benchmark type.

    Args:
        name: Benchmark name (used for CLI selection and config)
        benchmark_class: Benchmark class (must inherit from BenchmarkRunner)

    Raises:
        ValueError: If benchmark_class is not a BenchmarkRunner subclass

    Example:
        >>> from benchmarks import BenchmarkRunner, register_benchmark
        >>>
        >>> class MyBenchmark(BenchmarkRunner):
        ...     name = "custom_bench"
        ...
        ...     def run(self, sut_host, sut_port, output_dir, timeout_sec):
        ...         pass
        ...
        ...     def parse_results(self, output):
        ...         return {}
        >>>
        >>> register_benchmark("custom_bench", MyBenchmark)
    """
    if not issubclass(benchmark_class, BenchmarkRunner):
        raise ValueError(
            f"benchmark_class must inherit from BenchmarkRunner, got: {benchmark_class}"
        )

    if name in _BENCHMARK_REGISTRY:
        logger.warning(f"Overriding existing benchmark type: {name}")

    _BENCHMARK_REGISTRY[name] = benchmark_class
    logger.info(f"Registered benchmark type: {name}")


def unregister_benchmark(name: str) -> bool:
    """
    Unregister a benchmark type.

    Args:
        name: Benchmark name

    Returns:
        True if successfully unregistered
    """
    if name in _BENCHMARK_REGISTRY:
        del _BENCHMARK_REGISTRY[name]
        logger.info(f"Unregistered benchmark type: {name}")
        return True
    return False


def get_available_benchmarks() -> List[str]:
    """
    Get all available benchmark type names.

    Returns:
        List of benchmark names
    """
    return list(_BENCHMARK_REGISTRY.keys())


def get_benchmark_class(name: str) -> Optional[Type[BenchmarkRunner]]:
    """
    Get a benchmark class by name.

    Args:
        name: Benchmark name

    Returns:
        Benchmark class or None
    """
    return _BENCHMARK_REGISTRY.get(name.lower())


def is_benchmark_registered(name: str) -> bool:
    """
    Check if a benchmark type is registered.

    Args:
        name: Benchmark name

    Returns:
        True if registered
    """
    return name.lower() in _BENCHMARK_REGISTRY


def create_benchmark(
    benchmark_name: str,
    config: Optional[Dict[str, Any]] = None
) -> BenchmarkRunner:
    """
    Create a benchmark instance.

    Factory function for creating benchmark instances.

    Args:
        benchmark_name: Benchmark type name
        config: Optional configuration dictionary

    Returns:
        Benchmark instance

    Raises:
        ValueError: If benchmark name is not registered

    Example:
        >>> from benchmarks import create_benchmark
        >>>
        >>> bench = create_benchmark("sysbench", {"threads": [1, 4, 8]})
        >>> result = bench.run("127.0.0.1", 3306, Path("./output"), 600)
    """
    benchmark_name = benchmark_name.lower()
    if benchmark_name not in _BENCHMARK_REGISTRY:
        available = ", ".join(_BENCHMARK_REGISTRY.keys())
        raise ValueError(
            f"Unknown benchmark type: {benchmark_name}. Available types: {available}"
        )

    benchmark_class = _BENCHMARK_REGISTRY[benchmark_name]
    return benchmark_class(config)


def get_benchmarks_for_sut(sut_type: str) -> List[str]:
    """
    Get benchmarks that support a specific SUT type.

    Args:
        sut_type: SUT type name

    Returns:
        List of compatible benchmark names
    """
    compatible = []
    for name, benchmark_class in _BENCHMARK_REGISTRY.items():
        # Create temporary instance to check support
        instance = benchmark_class()
        if instance.supports_sut(sut_type):
            compatible.append(name)
    return compatible


def list_benchmarks_info() -> Dict[str, Dict[str, Any]]:
    """
    Get detailed information about all registered benchmarks.

    Returns:
        Dictionary with benchmark info, keyed by name
    """
    info = {}
    for name, benchmark_class in _BENCHMARK_REGISTRY.items():
        info[name] = {
            "class": benchmark_class.__name__,
            "module": benchmark_class.__module__,
            "description": getattr(benchmark_class, "description", ""),
            "supported_suts": getattr(benchmark_class, "supported_suts", []),
            "doc": (
                benchmark_class.__doc__.strip().split('\n')[0]
                if benchmark_class.__doc__
                else ""
            ),
        }
    return info


# Initialize registry with built-in benchmarks
_register_builtin_benchmarks()
