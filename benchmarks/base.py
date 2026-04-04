"""
Benchmark Runner Base Class

Defines the abstract interface that all benchmark implementations must follow.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class BenchmarkStatus(Enum):
    """Benchmark execution status."""

    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    RUNTIME_ERROR = "Runtime Error"
    SKIPPED = "Skipped"
    PENDING = "Pending"

    @classmethod
    def from_string(cls, s: str) -> "BenchmarkStatus":
        """Convert string to status enum."""
        mapping = {
            "accepted": cls.ACCEPTED,
            "pass": cls.ACCEPTED,
            "ok": cls.ACCEPTED,
            "wrong answer": cls.WRONG_ANSWER,
            "fail": cls.WRONG_ANSWER,
            "failed": cls.WRONG_ANSWER,
            "partial": cls.WRONG_ANSWER,
            "timeout": cls.TIME_LIMIT_EXCEEDED,
            "time limit exceeded": cls.TIME_LIMIT_EXCEEDED,
            "time_limit_exceeded": cls.TIME_LIMIT_EXCEEDED,
            "tle": cls.TIME_LIMIT_EXCEEDED,
            "runtime error": cls.RUNTIME_ERROR,
            "run time error": cls.RUNTIME_ERROR,  # backward compat
            "error": cls.RUNTIME_ERROR,
            "rte": cls.RUNTIME_ERROR,
            "skipped": cls.SKIPPED,
            "skip": cls.SKIPPED,
            "pending": cls.PENDING,
        }
        return mapping.get(s.lower().strip(), cls.RUNTIME_ERROR)


@dataclass
class BenchmarkResult:
    """
    Result from a benchmark run.

    Attributes:
        status: Overall status of the benchmark
        score: Numeric score (0.0 to 1.0 or absolute metric)
        metrics: Dictionary of measured metrics
        details: Human-readable details/summary
        raw_output: Raw benchmark output (if available)
        output_dir: Path to output directory
        error: Error message if failed
        elapsed_sec: Total elapsed time in seconds
    """

    status: BenchmarkStatus
    score: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    details: str = ""
    raw_output: str = ""
    output_dir: Optional[Path] = None
    error: Optional[str] = None
    elapsed_sec: float = 0.0
    workload_results: Dict[str, str] = field(default_factory=dict)

    def is_passed(self) -> bool:
        """Check if benchmark passed."""
        return self.status == BenchmarkStatus.ACCEPTED

    def is_failed(self) -> bool:
        """Check if benchmark failed (not skipped or pending)."""
        return self.status in (
            BenchmarkStatus.WRONG_ANSWER,
            BenchmarkStatus.TIME_LIMIT_EXCEEDED,
            BenchmarkStatus.RUNTIME_ERROR,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        d = {
            "status": self.status.value,
            "score": self.score,
            "metrics": self.metrics,
            "details": self.details,
            "output_dir": str(self.output_dir) if self.output_dir else None,
            "error": self.error,
            "elapsed_sec": self.elapsed_sec,
        }
        if self.workload_results:
            d["workload_results"] = self.workload_results
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BenchmarkResult":
        """Create from dictionary."""
        return cls(
            status=BenchmarkStatus.from_string(data.get("status", "error")),
            score=data.get("score", 0.0),
            metrics=data.get("metrics", {}),
            details=data.get("details", ""),
            raw_output=data.get("raw_output", ""),
            output_dir=Path(data["output_dir"]) if data.get("output_dir") else None,
            error=data.get("error"),
            elapsed_sec=data.get("elapsed_sec", 0.0),
            workload_results=data.get("workload_results", {}),
        )


class BenchmarkRunner(ABC):
    """
    Abstract base class for Benchmark Runner implementations.

    A benchmark runner represents a test suite that can:
    - Run against a System Under Test
    - Parse and aggregate results
    - Generate feedback for AI agents

    Subclasses must implement all abstract methods to define
    specific benchmarks (e.g., Sysbench, TPC-C, HTTP load testing).

    Attributes:
        name: Unique identifier for this benchmark
        description: Human-readable description
        supported_suts: List of SUT types this benchmark supports

    Example:
        >>> class SysbenchRunner(BenchmarkRunner):
        ...     name = "sysbench"
        ...     supported_suts = ["database"]
        ...
        ...     def run(self, sut, config, output_dir, timeout_sec):
        ...         # Run sysbench against database
        ...         pass
        ...
        ...     def parse_results(self, output):
        ...         # Parse sysbench output
        ...         return {}
    """

    # Benchmark name, subclasses must override
    name: str = "base"

    # Human-readable description
    description: str = "Base Benchmark Runner"

    # List of SUT types this benchmark supports
    supported_suts: List[str] = []

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the benchmark runner.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

    def supports_sut(self, sut_type: str) -> bool:
        """
        Check if this benchmark supports the given SUT type.

        Args:
            sut_type: SUT type name

        Returns:
            True if supported
        """
        if not self.supported_suts:
            return True  # Empty list means all SUTs supported
        return sut_type.lower() in [s.lower() for s in self.supported_suts]

    @abstractmethod
    def run(
        self,
        sut_host: str,
        sut_port: int,
        output_dir: Path,
        timeout_sec: int = 600,
        **kwargs
    ) -> BenchmarkResult:
        """
        Run the benchmark against a system.

        Args:
            sut_host: Host address of the system
            sut_port: Port of the system
            output_dir: Directory to store outputs
            timeout_sec: Timeout in seconds
            **kwargs: Additional benchmark-specific arguments

        Returns:
            BenchmarkResult with status and metrics
        """
        pass

    @abstractmethod
    def parse_results(self, output: str) -> Dict[str, Any]:
        """
        Parse benchmark output into structured metrics.

        Args:
            output: Raw benchmark output string

        Returns:
            Dictionary of parsed metrics
        """
        pass

    def planned_workload_count(self, **kwargs) -> int:
        """
        Return the number of individual workload results this benchmark will produce.

        Benchmarks that populate workload_results should override this to return
        the expected count. Default returns 1 (monolithic benchmark).
        """
        return 1

    def planned_workload_ids(self, **kwargs) -> List[str]:
        """
        Return stable workload identifiers for score planning.

        Benchmarks that emit repeated workload names across tiers can override
        this so the orchestrator can avoid double-counting the same logical
        workload in planned totals. Default returns an empty list, which means
        the orchestrator should fall back to planned_workload_count().
        """
        return []

    def get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration for this benchmark.

        Subclasses should override to provide sensible defaults.

        Returns:
            Default configuration dictionary
        """
        return {}

    def validate_config(self) -> List[str]:
        """
        Validate benchmark configuration.

        Returns:
            List of error messages (empty if valid)
        """
        return []

    def get_feedback_summary(self, result: BenchmarkResult) -> str:
        """
        Generate a feedback summary for AI agents.

        Args:
            result: Benchmark result

        Returns:
            Human-readable feedback string
        """
        lines = [
            f"Benchmark: {self.name}",
            f"Status: {result.status.value}",
            f"Score: {result.score:.2f}",
        ]

        if result.metrics:
            lines.append("Metrics:")
            for key, value in result.metrics.items():
                lines.append(f"  {key}: {value}")

        if result.error:
            lines.append(f"Error: {result.error}")

        if result.details:
            lines.append(f"Details: {result.details}")

        return "\n".join(lines)

    def prepare(self, sut_host: str, sut_port: int, **kwargs) -> bool:
        """
        Prepare benchmark (e.g., create schemas, load data).

        This is called before run() and can be used for setup tasks.

        Args:
            sut_host: Host address of the system
            sut_port: Port of the system
            **kwargs: Additional arguments

        Returns:
            True if preparation succeeded
        """
        return True

    def cleanup(self, sut_host: str, sut_port: int, **kwargs) -> bool:
        """
        Clean up after benchmark (e.g., drop schemas).

        This is called after run() and can be used for cleanup tasks.

        Args:
            sut_host: Host address of the system
            sut_port: Port of the system
            **kwargs: Additional arguments

        Returns:
            True if cleanup succeeded
        """
        return True
