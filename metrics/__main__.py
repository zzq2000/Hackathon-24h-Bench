"""CLI entrypoint: python -m metrics."""

from __future__ import annotations

import argparse
import json
import os
import sys

from metrics.aggregator import aggregate
from metrics.benchmark_linker import load_benchmarks
from metrics.report import print_summary, to_json


def _auto_detect_benchmark_dir(run_dir: str) -> str | None:
    """Try to find output/{run_id}/ from a run log directory."""
    run_id = os.path.basename(os.path.normpath(run_dir))
    # Check relative to CWD
    candidate = os.path.join("output", run_id)
    if os.path.isdir(candidate):
        return candidate
    # Check relative to parent of logs/runs/
    parent = os.path.dirname(os.path.dirname(os.path.dirname(run_dir)))
    if parent:
        candidate = os.path.join(parent, "output", run_id)
        if os.path.isdir(candidate):
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="metrics",
        description="Parse agent iteration logs and produce metrics reports.",
    )
    parser.add_argument(
        "run_dir",
        help="Path to the run log directory (logs/runs/{run_id})",
    )
    parser.add_argument(
        "-o", "--output",
        help="Write JSON report to this file path",
    )
    parser.add_argument(
        "--benchmark-dir",
        help="Benchmark output directory (output/{run_id}). Auto-detected if omitted.",
    )

    args = parser.parse_args()

    if not os.path.isdir(args.run_dir):
        print(f"Error: run directory not found: {args.run_dir}", file=sys.stderr)
        sys.exit(1)

    # Load benchmarks
    bench_dir = args.benchmark_dir or _auto_detect_benchmark_dir(args.run_dir)
    benchmarks = load_benchmarks(bench_dir) if bench_dir else []

    # Aggregate
    run_metrics = aggregate(args.run_dir, benchmarks)

    # Output
    if args.output:
        report = to_json(run_metrics)
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report written to {args.output}")

    print_summary(run_metrics)


if __name__ == "__main__":
    main()
