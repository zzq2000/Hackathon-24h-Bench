"""Link benchmark results from output directories to iterations."""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime

from metrics.models import BenchmarkSnapshot, IterationMetrics

_OUTPUT_DIR_RE = re.compile(r"^output_(\d+)$")


def load_benchmarks(benchmark_dir: str) -> list[BenchmarkSnapshot]:
    """Load all benchmark snapshots from an output/{run_id}/ directory.

    Reads output_N/meta.json files, sorted by test_index.
    """
    if not os.path.isdir(benchmark_dir):
        return []

    snapshots: list[BenchmarkSnapshot] = []
    for entry in os.listdir(benchmark_dir):
        m = _OUTPUT_DIR_RE.match(entry)
        if not m:
            continue
        meta_path = os.path.join(benchmark_dir, entry, "meta.json")
        if not os.path.isfile(meta_path):
            continue
        try:
            with open(meta_path) as f:
                meta = json.load(f)
            snapshots.append(BenchmarkSnapshot(
                test_index=meta.get("test_index", int(m.group(1))),
                score=meta.get("score", 0.0),
                overall_status=meta.get("overall_status", "Unknown"),
                passed_count=meta.get("passed_count", 0),
                total_count=meta.get("total_count", 0),
                test_start=meta.get("test_start", ""),
                test_end=meta.get("test_end", ""),
                error=meta.get("error"),
                snapshot_time=meta.get("snapshot_time"),
            ))
        except (json.JSONDecodeError, OSError):
            continue

    snapshots.sort(key=lambda s: s.test_index)
    return snapshots


def _git_commit_local_time(git_dir: str, commit_sha: str) -> str | None:
    """Get a commit's time as a local-timezone ISO string via git log.

    Uses ``git log --format=%ct`` to get the committer epoch, then
    converts to a local-time ISO string (matching the host timezone that
    benchmark meta.json timestamps use).
    """
    try:
        r = subprocess.run(
            ["git", "-C", git_dir, "log", "-1", "--format=%ct", commit_sha],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0:
            return None
        epoch = int(r.stdout.strip())
        return datetime.fromtimestamp(epoch).isoformat()
    except (ValueError, subprocess.TimeoutExpired, OSError):
        return None


def resolve_iteration_local_time(
    iteration: IterationMetrics,
    workspace_git_dir: str | None = None,
) -> str | None:
    """Resolve an iteration timestamp onto the host-local wall clock.

    Preferred source is the snapshot commit epoch converted to local time,
    because snapshot files may be written in a container timezone while
    benchmark metadata is written on the host. Falls back to raw snapshot
    or iteration timestamps when commit resolution is unavailable.
    """
    local_ts: str | None = None

    if workspace_git_dir and iteration.snapshot_commit:
        local_ts = _git_commit_local_time(workspace_git_dir, iteration.snapshot_commit)

    if local_ts is None and iteration.snapshot_timestamp:
        local_ts = iteration.snapshot_timestamp

    if local_ts is None and iteration.iteration_timestamp:
        local_ts = iteration.iteration_timestamp

    return local_ts


def link_benchmarks_to_iterations(
    benchmarks: list[BenchmarkSnapshot],
    iterations: list[IterationMetrics],
    workspace_git_dir: str | None = None,
) -> None:
    """Link each benchmark to the latest iteration whose commit time
    is <= the benchmark's snapshot_time.

    Uses git commit epochs (converted to host-local time) to avoid
    timezone mismatches between container-written snapshot timestamps
    and host-written benchmark timestamps.

    Falls back to raw snapshot_timestamp comparison when workspace_git_dir
    is not available or commits cannot be resolved.

    Modifies benchmarks in place by setting ``linked_iteration``.
    """
    if not benchmarks or not iterations:
        return

    # Build sorted list of (local_time_str, iteration_index).
    timed_iters: list[tuple[str, int]] = []

    for im in iterations:
        local_ts = resolve_iteration_local_time(im, workspace_git_dir=workspace_git_dir)
        if local_ts:
            timed_iters.append((local_ts, im.iteration))

    if not timed_iters:
        return
    timed_iters.sort(key=lambda t: t[0])

    for bench in benchmarks:
        snap_time = bench.snapshot_time
        if not snap_time:
            continue
        # Find the latest iteration snapshot <= benchmark snapshot_time.
        best_iter: int | None = None
        for ts, iter_idx in reversed(timed_iters):
            if ts <= snap_time:
                best_iter = iter_idx
                break
        bench.linked_iteration = best_iter
