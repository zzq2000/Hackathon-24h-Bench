"""
Test Runner Module

Provides generic test orchestration for running benchmarks against
System Under Test implementations.

Example:
    >>> from test_runner import TestOrchestrator
    >>> from sut import create_sut
    >>>
    >>> sut = create_sut("database", Path("./workspace/database/database_gpt"))
    >>> orchestrator = TestOrchestrator(sut, benchmarks=["sysbench", "tpcc"])
    >>> result = orchestrator.run_cycle(test_index=1)
"""

from .core import TestOrchestrator, TestCycleResult
from .scheduler import TestScheduler
from .reporter import TestReporter

__all__ = [
    "TestOrchestrator",
    "TestCycleResult",
    "TestScheduler",
    "TestReporter",
]
