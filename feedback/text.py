"""
Text Feedback Formatter

Implements the current last_brief.txt format for backward compatibility.
"""

import logging
from pathlib import Path
from typing import Optional

from .base import FeedbackFormatter, FeedbackData

logger = logging.getLogger(__name__)


class TextFeedbackFormatter(FeedbackFormatter):
    """
    Text-based feedback formatter.

    Produces output in the format:
        version_id: <id>
        agent: <agent>
        snapshot_time: <time>
        test_start: <time>
        test_end: <time>
        overall: <status> [- error details]
        score: <pct>% (<passed>/<total>)

    This matches the existing last_brief.txt format for backward compatibility.
    """

    name = "text"
    extension = ".txt"

    def format(self, data: FeedbackData) -> str:
        """
        Format feedback data into text.

        Args:
            data: Structured feedback data

        Returns:
            Formatted text string
        """
        lines = []

        # Header info
        lines.append(f"version_id: {data.version_id}")
        lines.append(f"agent: {data.agent}")
        lines.append(f"snapshot_time: {data.snapshot_time}")
        lines.append(f"test_start: {data.test_start}")
        lines.append(f"test_end: {data.test_end}")

        # Overall status with error details (truncated to avoid leaking
        # benchmark internals like full SQL queries or test data)
        overall_line = f"overall: {data.overall_status}"
        if data.error_message:
            err = data.error_message
            if len(err) > 120:
                err = err[:120] + "..."
            overall_line = f"{overall_line} - {err}"
        lines.append(overall_line)

        # Score
        lines.append(
            f"score: {data.score:.1f}% ({data.passed_count}/{data.total_count})"
        )

        # Tier/suite breakdown
        if data.tiers:
            lines.append("")
            lines.append("--- tiers ---")
            for tier in data.tiers:
                tier_name = tier.get("tier", "unknown")
                tier_status = tier.get("status", "unknown")
                suites = tier.get("suites", {})

                # Check if tier is skipped (handles both "Skipped" and "SKIPPED")
                if tier_status.upper() in ("SKIPPED", "SKIP"):
                    lines.append(f"{tier_name}: Skipped")
                    continue

                # Count pass/total excluding SKIP suites
                if isinstance(suites, dict):
                    non_skip = {k: v for k, v in suites.items() if v != "SKIP"}
                    tier_passed = sum(1 for v in non_skip.values() if v == "PASS")
                    tier_total = len(non_skip)
                else:
                    non_skip = {}
                    tier_passed = 0
                    tier_total = 0

                tier_line = f"{tier_name}: {tier_status} ({tier_passed}/{tier_total})"

                # Append first error for failed tiers
                tier_error = tier.get("error") or tier.get("detail")
                if tier_error and tier_status not in ("Accepted",):
                    truncated = tier_error[:120]
                    if len(tier_error) > 120:
                        truncated += "..."
                    tier_line += f" -- {truncated}"

                lines.append(tier_line)

                # Group suites by benchmark prefix (split on first ":")
                grouped: dict = {}
                for suite_name, suite_status in non_skip.items():
                    if ":" in suite_name:
                        bench, wl = suite_name.split(":", 1)
                    else:
                        bench = suite_name
                        wl = None
                    grouped.setdefault(bench, []).append((wl, suite_status))

                for bench_name, entries in grouped.items():
                    grp_passed = sum(1 for _, s in entries if s == "PASS")
                    grp_total = len(entries)
                    grp_line = f"  {bench_name}: {grp_passed}/{grp_total} passed"

                    # List failed workloads if 1-5 failures
                    failed = [wl for wl, s in entries if s != "PASS" and wl is not None]
                    if 1 <= len(failed) <= 5:
                        grp_line += f" [FAIL: {', '.join(failed)}]"

                    lines.append(grp_line)

        return "\n".join(lines) + "\n"

    def format_detailed(self, data: FeedbackData) -> str:
        """
        Format feedback data with detailed tier information.

        Args:
            data: Structured feedback data

        Returns:
            Detailed formatted text string
        """
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append(f"Test Report: {data.version_id}")
        lines.append("=" * 60)
        lines.append("")

        # Summary
        lines.append("[Summary]")
        lines.append(f"  Agent: {data.agent} ({data.agent_type})")
        lines.append(f"  Model: {data.agent_model}")
        lines.append(f"  Snapshot: {data.snapshot_time}")
        lines.append(f"  Test Window: {data.test_start} -> {data.test_end}")
        lines.append(f"  Overall: {data.overall_status}")
        lines.append(
            f"  Score: {data.score:.1f}% ({data.passed_count}/{data.total_count})"
        )
        lines.append("")

        # Tier details
        if data.tiers:
            lines.append("[Tier Results]")
            for tier in data.tiers:
                tier_name = tier.get("tier", "unknown")
                tier_status = tier.get("status", "unknown")
                lines.append(f"  {tier_name}: {tier_status}")

                suites = tier.get("suites", {})
                if isinstance(suites, dict):
                    # Group by benchmark prefix for readability
                    grouped = {}
                    for suite_name, suite_status in suites.items():
                        if ":" in suite_name:
                            bench, wl = suite_name.split(":", 1)
                            grouped.setdefault(bench, []).append((wl, suite_status))
                        else:
                            grouped.setdefault(suite_name, []).append((None, suite_status))

                    for bench_name, entries in grouped.items():
                        if len(entries) == 1 and entries[0][0] is None:
                            lines.append(f"    - {bench_name}: {entries[0][1]}")
                        else:
                            pass_count = sum(1 for _, s in entries if s == "PASS")
                            lines.append(f"    - {bench_name}: {pass_count}/{len(entries)} passed")
                            for wl_name, wl_status in entries:
                                label = wl_name if wl_name else bench_name
                                lines.append(f"      - {label}: {wl_status}")

                if tier.get("reason"):
                    lines.append(f"    Reason: {tier.get('reason')}")
                if tier.get("detail"):
                    lines.append(f"    Detail: {tier.get('detail')}")
            lines.append("")

        # Error section
        if data.error_message:
            lines.append("[Error]")
            lines.append(f"  {data.error_message}")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines) + "\n"


class JsonFeedbackFormatter(FeedbackFormatter):
    """
    JSON-based feedback formatter.

    Produces machine-readable JSON output.
    """

    name = "json"
    extension = ".json"

    def format(self, data: FeedbackData) -> str:
        """
        Format feedback data into JSON.

        Args:
            data: Structured feedback data

        Returns:
            JSON string
        """
        import json
        return json.dumps(data.to_dict(), indent=2, ensure_ascii=False)
