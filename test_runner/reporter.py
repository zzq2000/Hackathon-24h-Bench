"""
Test Reporter Module

Provides result aggregation and reporting functionality.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from .core import TestCycleResult, TierResult

logger = logging.getLogger(__name__)


class TestReporter:
    """
    Test result reporter.

    Handles:
    - Result aggregation across multiple cycles
    - Summary generation
    - Error extraction from logs
    """
    __test__ = False

    def __init__(self, output_dir: Path):
        """
        Initialize reporter.

        Args:
            output_dir: Base output directory
        """
        self.output_dir = output_dir
        self._results: List[TestCycleResult] = []

    def add_result(self, result: TestCycleResult) -> None:
        """Add a test cycle result."""
        self._results.append(result)

    def get_results(self) -> List[TestCycleResult]:
        """Get all results."""
        return self._results.copy()

    def get_latest_result(self) -> Optional[TestCycleResult]:
        """Get the most recent result."""
        return self._results[-1] if self._results else None

    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate summary of all test results.

        Returns:
            Summary dictionary
        """
        if not self._results:
            return {"total_cycles": 0, "results": []}

        # Calculate statistics
        total = len(self._results)
        passed = sum(1 for r in self._results if r.overall_status == "Accepted")
        failed = total - passed

        # Score progression
        scores = [r.score for r in self._results]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        max_score = max(scores) if scores else 0.0

        return {
            "total_cycles": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0.0,
            "average_score": avg_score,
            "max_score": max_score,
            "score_progression": scores,
            "results": [r.to_dict() for r in self._results],
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

    def write_summary(self, path: Optional[Path] = None) -> Path:
        """
        Write summary to file.

        Args:
            path: Output path (default: output_dir/summary.json)

        Returns:
            Path to written file
        """
        if path is None:
            path = self.output_dir / "summary.json"

        summary = self.generate_summary()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(summary, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info(f"Wrote summary to {path}")
        return path

    def extract_first_error(self, result: TestCycleResult) -> Optional[str]:
        """
        Extract the first error from a test result.

        Args:
            result: Test cycle result

        Returns:
            First error message or None
        """
        # Check direct error
        if result.error:
            return result.error

        # Check tier errors
        for tier in result.tiers:
            if tier.error:
                return tier.error
            if tier.detail:
                return tier.detail

        # Try to extract from raw logs
        if result.meta.get("output_root"):
            output_root = Path(result.meta["output_root"])
            error = self._extract_error_from_logs(output_root)
            if error:
                return error

        return None

    def _extract_error_from_logs(self, output_dir: Path) -> Optional[str]:
        """Extract first error from raw log files."""
        raw_dir = output_dir / "raw"

        # Also check benchmark-namespaced raw dirs (e.g. L0/mq_bench/raw/)
        candidate_dirs = [raw_dir]
        for bench_dir in output_dir.iterdir() if output_dir.exists() else []:
            nested = bench_dir / "raw"
            if bench_dir.is_dir() and nested.is_dir():
                candidate_dirs.append(nested)

        # Patterns for different log types
        log_patterns = []
        for d in candidate_dirs:
            if d.exists():
                log_patterns.extend([
                    d / "sysbench" / "*.log",
                    d / "tpcc" / "*.log",
                    d / "tpch" / "*.log",
                    d / "pika" / "*.log",
                ])

        # Error patterns (including pytest "E   <exception>" lines)
        error_re = re.compile(
            r"(FATAL:\s*\S.*|ERROR:\s*\S.*|(?<!\w)Error:\s*\S.*|^E\s+\S+Error\b.*|^E\s+\S+Exception\b.*)",
            re.MULTILINE
        )
        # Exclude patterns (statistics lines)
        exclude_re = re.compile(
            r"(ignored\s+errors|reconnect\s+errors|other\s+errors|total\s+errors):\s*\d+",
            re.IGNORECASE
        )

        for pattern in log_patterns:
            for log_file in sorted(pattern.parent.glob(pattern.name)):
                try:
                    content = log_file.read_text(encoding="utf-8", errors="replace")
                    for line in content.splitlines():
                        if exclude_re.search(line):
                            continue
                        match = error_re.search(line)
                        if match:
                            return line.strip()
                except Exception as e:
                    logger.debug(f"Failed to read log {log_file}: {e}")

        return None

    def classify_result(self, result: TestCycleResult) -> Dict[str, Any]:
        """
        Classify a test result for reporting.

        Args:
            result: Test cycle result

        Returns:
            Classification dictionary
        """
        classification = {
            "status": result.overall_status,
            "suites": {},
        }

        # Map status to standard values
        status_map = {
            "Accepted": "PASS",
            "Wrong Answer": "PARTIAL",
            "Time Limit Exceeded": "TIME_LIMIT_EXCEEDED",
            "Run Time Error": "ERROR",
        }
        classification["status"] = status_map.get(
            result.overall_status,
            result.overall_status
        )

        # Aggregate suite results
        for tier in result.tiers:
            for suite, status in tier.suites.items():
                if suite not in classification["suites"]:
                    classification["suites"][suite] = status
                elif classification["suites"][suite] == "PASS" and status != "PASS":
                    classification["suites"][suite] = status

        return classification

    def format_brief(self, result: TestCycleResult) -> str:
        """
        Format a brief text summary.

        Args:
            result: Test cycle result

        Returns:
            Brief summary string
        """
        lines = [
            f"version_id: {result.cycle_id}",
            f"agent: {result.meta.get('agent', 'unknown')}",
            f"snapshot_time: {result.meta.get('snapshot_time', '')}",
            f"test_start: {result.test_start}",
            f"test_end: {result.test_end}",
        ]

        # Overall status with error
        overall_line = f"overall: {result.overall_status}"
        if result.overall_status == "Wrong Answer":
            error = self.extract_first_error(result)
            if error:
                overall_line = f"{overall_line} - {error}"
        lines.append(overall_line)

        # Score
        lines.append(
            f"score: {result.score:.1f}% ({result.passed_count}/{result.total_count})"
        )

        return "\n".join(lines) + "\n"

    def generate_markdown_report(self, result: TestCycleResult) -> str:
        """
        Generate a Markdown report for a test result.

        Args:
            result: Test cycle result

        Returns:
            Markdown formatted report
        """
        lines = [
            f"# Test Report: {result.cycle_id}",
            "",
            "## Summary",
            "",
            f"- **Status**: {result.overall_status}",
            f"- **Score**: {result.score:.1f}% ({result.passed_count}/{result.total_count})",
            f"- **Test Start**: {result.test_start}",
            f"- **Test End**: {result.test_end}",
            "",
        ]

        # Tier results table
        lines.extend([
            "## Tier Results",
            "",
            "| Tier | Status | Suites |",
            "|------|--------|--------|",
        ])

        for tier in result.tiers:
            suites_str = ", ".join(
                f"{s}: {st}" for s, st in tier.suites.items()
            ) or "N/A"
            lines.append(f"| {tier.tier} | {tier.status} | {suites_str} |")

        lines.append("")

        # Error section
        error = self.extract_first_error(result)
        if error:
            lines.extend([
                "## Error",
                "",
                f"```",
                error,
                "```",
                "",
            ])

        return "\n".join(lines)
