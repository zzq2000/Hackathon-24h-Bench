"""JSON output and CLI table rendering for metrics."""

from __future__ import annotations

import dataclasses
import json
from typing import Any

from metrics.models import BenchmarkSnapshot, RunMetrics


def to_json(run_metrics: RunMetrics) -> dict[str, Any]:
    """Convert RunMetrics to a JSON-serializable dict."""
    return dataclasses.asdict(run_metrics)


def _fmt_num(n: int | float) -> str:
    """Format a number with comma separators."""
    if isinstance(n, float):
        return f"{n:,.1f}"
    return f"{n:,}"


def _fmt_optional_num(n: int | float | None) -> str:
    """Format a number or return N/A for unknown values."""
    if n is None:
        return "N/A"
    return _fmt_num(n)


def print_summary(run_metrics: RunMetrics) -> None:
    """Print a CLI summary table to stdout."""
    rm = run_metrics
    print(f"=== Run Metrics: {rm.run_id} ===")
    print(f"Agent: {rm.agent} | Model: {rm.model}")
    print()

    # Build a lookup: iteration index → list of benchmark scores linked to it
    iter_benchmarks: dict[int, list[BenchmarkSnapshot]] = {}
    unlinked_benchmarks: list[BenchmarkSnapshot] = []
    for b in rm.benchmarks:
        if b.linked_iteration is not None:
            iter_benchmarks.setdefault(b.linked_iteration, []).append(b)
        else:
            unlinked_benchmarks.append(b)

    # Check if any iteration has cost data
    has_cost = any(im.cost_usd is not None for im in rm.iterations)

    # Header
    cost_hdr = f"  {'Cost($)':>8}" if has_cost else ""
    header = (
        f"{'Iter':>4}  {'Duration':>9}  {'Tokens(in/out/total)':>24}  "
        f"{'Steps':>5}  {'Tools':>5}  {'Commits':>7}  {'CodeΔ':>7}"
        f"{cost_hdr}  {'Bench Score':>11}"
    )
    cost_sep = f"  {'────────':>8}" if has_cost else ""
    sep = (
        f"{'────':>4}  {'─────────':>9}  {'────────────────────────':>24}  "
        f"{'─────':>5}  {'─────':>5}  {'───────':>7}  {'───────':>7}"
        f"{cost_sep}  {'───────────':>11}"
    )
    print(header)
    print(sep)

    # Per-iteration rows
    for im in rm.iterations:
        tokens_str = f"{_fmt_num(im.tokens_input)}/{_fmt_num(im.tokens_output)}/{_fmt_num(im.tokens_total)}"

        # Show benchmark scores linked to this iteration
        linked = iter_benchmarks.get(im.iteration, [])
        if linked:
            score_str = ", ".join(f"{b.score:.1f}%" for b in linked)
        else:
            score_str = "N/A"

        cost_col = ""
        if has_cost:
            cost_col = f"  {im.cost_usd:>8.2f}" if im.cost_usd is not None else f"  {'N/A':>8}"
        row = (
            f"{im.iteration:>4}  {im.duration_seconds:>8.1f}s  {tokens_str:>24}  "
            f"{im.step_count:>5}  {im.total_tool_calls:>5}  {im.commit_count:>7}  "
            f"{_fmt_optional_num(im.workspace_loc_added):>7}{cost_col}  {score_str:>11}"
        )
        print(row)

    # Print benchmarks that couldn't be linked to any iteration
    for b in unlinked_benchmarks:
        score_str = f"{b.score:.1f}%"
        cost_blank = f"  {'':>8}" if has_cost else ""
        print(f"{'?':>4}  {'':>9}  {'':>24}  {'':>5}  {'':>5}  {'':>7}  {'':>7}{cost_blank}  {score_str:>11}")

    # Totals
    print()
    print("─── Totals ───")
    print(f"Total Duration:   {_fmt_num(rm.total_duration_seconds)}s")
    print(
        f"Total Tokens:     {_fmt_num(rm.total_tokens)} "
        f"(input: {_fmt_num(sum(i.tokens_input for i in rm.iterations))}, "
        f"output: {_fmt_num(sum(i.tokens_output for i in rm.iterations))}, "
        f"cache_read: {_fmt_num(sum(i.tokens_cache_read for i in rm.iterations))})"
    )

    # Tool call summary
    tool_parts = ", ".join(
        f"{name}: {count}" for name, count in rm.tool_call_summary.items()
    )
    print(f"Total Tool Calls: {_fmt_num(rm.total_tool_calls)} ({tool_parts})")
    print(f"Total Commits:    {_fmt_num(rm.total_commits)}")
    print(
        f"Total Commands:   {_fmt_num(rm.total_commands)} "
        f"(ok: {_fmt_num(rm.total_command_successes)}, "
        f"fail: {_fmt_num(rm.total_command_failures)}, "
        f"timeout: {_fmt_num(rm.total_command_timeouts)})"
    )
    print(
        f"File Ops:         reads {_fmt_num(rm.total_files_read)}, "
        f"writes {_fmt_num(rm.total_files_written)}"
    )
    print(
        f"Tests Observed:   collected {_fmt_num(rm.total_tests_collected)}, "
        f"passed {_fmt_num(rm.total_tests_passed)}"
    )
    if rm.peak_context_window_used_tokens is not None:
        print(f"Peak Context Use: {_fmt_num(rm.peak_context_window_used_tokens)} tokens")
    total_cost = sum(im.cost_usd for im in rm.iterations if im.cost_usd is not None)
    if total_cost > 0:
        print(f"Total Cost:       ${total_cost:,.2f}")
    print(f"Total Code Lines Changed: {_fmt_optional_num(rm.total_workspace_loc_added)}")

    # Benchmark progression
    if rm.benchmarks:
        progression = " → ".join(f"{b.score:.1f}%" for b in rm.benchmarks)
        print(f"Benchmark Progression: {progression}")

    if rm.warnings:
        print()
        print("Warnings:")
        seen: set[str] = set()
        for warning in rm.warnings:
            if warning in seen:
                continue
            seen.add(warning)
            print(f"- {warning}")
