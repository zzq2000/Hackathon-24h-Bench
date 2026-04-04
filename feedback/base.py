"""
Feedback Formatter Base Class

Defines the abstract interface for formatting benchmark feedback.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class FeedbackData:
    """
    Structured feedback data from a test cycle.

    Attributes:
        version_id: Unique identifier for this test version
        run_id: Run identifier (aligned with logs/runs)
        test_index: Test cycle index
        agent: Agent name
        agent_type: Agent type (codex, claude, gemini)
        agent_model: Model name
        snapshot_time: When the snapshot was taken
        test_start: Test start time
        test_end: Test end time
        overall_status: Overall test status
        tiers: List of tier results
        score: Score percentage
        passed_count: Number of passed tests
        total_count: Total number of tests
        error_message: First error message (if any)
        extra: Additional data
    """

    version_id: str = ""
    run_id: str = ""
    test_index: int = 0
    agent: str = ""
    agent_type: str = ""
    agent_model: str = ""
    snapshot_time: str = ""
    test_start: str = ""
    test_end: str = ""
    overall_status: str = ""
    tiers: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0
    passed_count: int = 0
    total_count: int = 0
    error_message: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_meta(cls, meta: Dict[str, Any]) -> "FeedbackData":
        """Create from test runner meta dictionary."""
        tiers = meta.get("tiers", [])

        # Use pre-calculated counts from test runner if available
        total_count = meta.get("total_count", 0)
        passed_count = meta.get("passed_count", 0)
        score = meta.get("score", 0.0)

        if total_count == 0:
            # Fallback: count from suite results directly
            for t in tiers:
                suites = t.get("suites", {})
                if isinstance(suites, dict):
                    for _, status in suites.items():
                        if status == "SKIP":
                            continue
                        total_count += 1
                        if status == "PASS":
                            passed_count += 1
            score = (passed_count / total_count) * 100.0 if total_count > 0 else 0.0

        # Extract error message
        error_message = None
        overall = meta.get("overall", "")
        if overall in ("Wrong Answer", "FAIL", "PARTIAL"):
            for tier_entry in tiers:
                if tier_entry.get("reason") == "preflight_failed":
                    error_message = tier_entry.get("detail")
                    break
                if tier_entry.get("status") == "Wrong Answer":
                    error_message = tier_entry.get("error")
                    break

        return cls(
            version_id=meta.get("version_id", meta.get("cycle_id", "")),
            run_id=meta.get("run_id", ""),
            test_index=meta.get("test_index", 0),
            agent=meta.get("agent", ""),
            agent_type=meta.get("agent_type", ""),
            agent_model=meta.get("agent_model", ""),
            snapshot_time=meta.get("snapshot_time", ""),
            test_start=meta.get("test_start", ""),
            test_end=meta.get("test_end", ""),
            overall_status=overall,
            tiers=tiers,
            score=score,
            passed_count=passed_count,
            total_count=total_count,
            error_message=error_message,
            extra=meta,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version_id": self.version_id,
            "run_id": self.run_id,
            "test_index": self.test_index,
            "agent": self.agent,
            "agent_type": self.agent_type,
            "agent_model": self.agent_model,
            "snapshot_time": self.snapshot_time,
            "test_start": self.test_start,
            "test_end": self.test_end,
            "overall_status": self.overall_status,
            "tiers": self.tiers,
            "score": self.score,
            "passed_count": self.passed_count,
            "total_count": self.total_count,
            "error_message": self.error_message,
            "extra": self.extra,
        }


class FeedbackFormatter(ABC):
    """
    Abstract base class for feedback formatters.

    A feedback formatter transforms structured benchmark results
    into a format consumable by AI code agents.

    Subclasses must implement format() and optionally write().
    """

    # Formatter name
    name: str = "base"

    # File extension for output
    extension: str = ".txt"

    @abstractmethod
    def format(self, data: FeedbackData) -> str:
        """
        Format feedback data into a string.

        Args:
            data: Structured feedback data

        Returns:
            Formatted feedback string
        """
        pass

    def write(self, path: Path, data: FeedbackData) -> bool:
        """
        Write formatted feedback to a file.

        Args:
            path: Output file path
            data: Structured feedback data

        Returns:
            True if written successfully
        """
        try:
            content = self.format(data)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            logger.info(f"Wrote feedback to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write feedback to {path}: {e}")
            return False

    def read(self, path: Path) -> Optional[str]:
        """
        Read feedback from a file.

        Args:
            path: File path

        Returns:
            Feedback content or None
        """
        try:
            if path.exists():
                return path.read_text(encoding="utf-8").strip()
        except Exception as e:
            logger.warning(f"Failed to read feedback from {path}: {e}")
        return None
