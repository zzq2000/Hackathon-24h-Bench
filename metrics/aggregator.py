"""Aggregate per-iteration metrics into run-level totals."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
from collections import Counter

from metrics.benchmark_linker import link_benchmarks_to_iterations
from metrics.models import BenchmarkSnapshot, IterationMetrics, RunMetrics
from metrics.parsers import get_parser


_CODE_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".cs", ".css", ".go", ".h", ".hpp", ".html",
    ".java", ".js", ".jsx", ".kt", ".kts", ".php", ".proto", ".py",
    ".pyi", ".rb", ".rs", ".sass", ".scala", ".scss", ".sh", ".sql",
    ".svelte", ".swift", ".ts", ".tsx", ".vue", ".xml", ".yml", ".yaml",
    ".zsh",
}
_CODE_FILENAMES = {
    "Dockerfile", "Makefile", "Justfile", "Procfile",
}
_EXCLUDED_PATH_PARTS = {
    ".git", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".venv", "venv", "node_modules", "last_brief", "last-brief", "data",
    "wal", "spec",
}
_EXCLUDED_BASENAMES = {
    ".coverage",
}
_EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def _normalize_diff_path(path: str) -> str:
    """Normalize a git numstat path, keeping the destination for renames."""
    normalized = path.strip().strip('"').replace("\\", "/")
    if "=>" in normalized:
        normalized = normalized.split("=>", 1)[1].strip()
    normalized = normalized.replace("{", "").replace("}", "")
    return normalized.strip()


def _is_code_path(path: str) -> bool:
    """Return True when the diff path looks like a source-code file."""
    normalized = _normalize_diff_path(path)
    if not normalized:
        return False

    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return False

    if any(part in _EXCLUDED_PATH_PARTS for part in parts[:-1]):
        return False

    basename = parts[-1]
    if basename in _EXCLUDED_BASENAMES:
        return False

    if basename in _CODE_FILENAMES:
        return True

    return Path(basename).suffix.lower() in _CODE_EXTENSIONS


def _find_workspace_git_dir(run_id: str) -> str | None:
    """Find the workspace git directory for a run_id.

    The workspace path follows the convention:
        workspace/{system_type}/{run_id}/
    where system_type is a prefix of run_id (e.g. "database", "message_queue").

    Tries matching against actual subdirectories under workspace/ to handle
    system types that contain underscores (e.g. "message_queue", "http_server").
    """
    workspace = "workspace"
    if not os.path.isdir(workspace):
        return None

    # Try each subdirectory of workspace/ as a potential system_type prefix
    for entry in os.listdir(workspace):
        if run_id.startswith(entry + "_"):
            candidate = os.path.join(workspace, entry, run_id)
            if os.path.isdir(os.path.join(candidate, ".git")):
                return candidate

    return None


def _load_snapshot(snapshots_dir: str, iteration: int) -> tuple[str | None, str | None]:
    """Load commit SHA and timestamp from a snapshot file.

    Returns (commit, timestamp) tuple.
    """
    path = os.path.join(snapshots_dir, f"iter_{iteration:03d}.json")
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path) as f:
            data = json.load(f)
        return data.get("commit"), data.get("timestamp")
    except (json.JSONDecodeError, OSError):
        return None, None


def _load_baseline_snapshot(run_dir: str) -> tuple[str | None, str | None]:
    """Load commit SHA and timestamp from baseline_snapshot.json when present."""
    path = os.path.join(run_dir, "baseline_snapshot.json")
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path) as f:
            data = json.load(f)
        return data.get("commit"), data.get("timestamp")
    except (json.JSONDecodeError, OSError):
        return None, None


def _load_snapshot_commit_map(snapshots_dir: str) -> dict[int, str]:
    """Load iteration -> commit mapping from snapshots directory."""
    if not os.path.isdir(snapshots_dir):
        return {}

    mapping: dict[int, str] = {}
    for fname in os.listdir(snapshots_dir):
        match = re.match(r"^iter_(\d+)\.json$", fname)
        if not match:
            continue
        try:
            iteration = int(match.group(1))
        except ValueError:
            continue
        path = os.path.join(snapshots_dir, fname)
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        commit = data.get("commit")
        if isinstance(commit, str) and commit.strip():
            mapping[iteration] = commit.strip()

    return mapping


def _short_sha(commit: str | None) -> str:
    """Return a short, human-readable commit reference."""
    if not commit:
        return "missing"
    return commit[:12]


def _git_changed_code_lines_between(
    git_dir: str,
    old_commit: str,
    new_commit: str,
) -> tuple[int | None, str | None]:
    """Get changed code line count (added + deleted) between two commits."""
    try:
        result = subprocess.run(
            ["git", "diff", "--numstat", old_commit, new_commit],
            cwd=git_dir,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return None, str(exc)

    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip() or "git diff failed"
        return None, message

    total_changed = 0
    for line in result.stdout.splitlines():
        # Format: "<added>\t<deleted>\t<path>"
        cols = line.split("\t", 2)
        if len(cols) < 3:
            continue
        added = cols[0].strip()
        deleted = cols[1].strip()
        path = cols[2].strip()
        if not _is_code_path(path):
            continue
        if added.isdigit():
            total_changed += int(added)
        if deleted.isdigit():
            total_changed += int(deleted)
    return total_changed, None


def _git_first_parent_commit(git_dir: str, commit: str) -> str | None:
    """Return the first parent commit SHA, or None for a root commit."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", f"{commit}^"],
            cwd=git_dir,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if result.returncode != 0:
        return None

    parent = result.stdout.strip()
    return parent or None


def _attach_workspace_loc_added(
    run_dir: str,
    iterations: list[IterationMetrics],
    workspace_git_dir: str | None,
) -> None:
    """Attach per-iteration code line changes using snapshot commits."""
    if not iterations or not workspace_git_dir:
        return

    snap_dir = os.path.join(run_dir, "snapshots")
    snapshot_commits = _load_snapshot_commit_map(snap_dir)
    baseline_snapshot_commit, _ = _load_baseline_snapshot(run_dir)
    prev_commit: str | None = None

    for im in iterations:
        current_commit = im.snapshot_commit
        if not current_commit:
            im.workspace_loc_added = None
            im.workspace_loc_issue = (
                f"CodeΔ unavailable for iter {im.iteration}: missing snapshot commit"
            )
            continue

        baseline_commit = prev_commit
        if baseline_commit is None and im.iteration == 0:
            baseline_commit = baseline_snapshot_commit
        # For first parsed iteration, prefer direct previous snapshot (e.g. iter_000).
        if baseline_commit is None:
            baseline_commit = snapshot_commits.get(im.iteration - 1)
        # Historical runs may be missing the previous snapshot linkage. In that
        # case, fall back to the snapshot commit's first parent before using the
        # empty tree for a root snapshot.
        if baseline_commit is None:
            baseline_commit = _git_first_parent_commit(workspace_git_dir, current_commit)

        if baseline_commit:
            changed, diff_issue = _git_changed_code_lines_between(
                workspace_git_dir,
                baseline_commit,
                current_commit,
            )
            compared_from = _short_sha(baseline_commit)
        else:
            changed, diff_issue = _git_changed_code_lines_between(
                workspace_git_dir,
                _EMPTY_TREE_SHA,
                current_commit,
            )
            compared_from = "empty-tree"

        if diff_issue is not None:
            im.workspace_loc_added = None
            im.workspace_loc_issue = (
                f"CodeΔ unavailable for iter {im.iteration}: failed to diff "
                f"{compared_from}..{_short_sha(current_commit)} ({diff_issue})"
            )
        else:
            im.workspace_loc_added = changed
            im.workspace_loc_issue = None

        prev_commit = current_commit


def _parse_iterations(run_dir: str) -> list[IterationMetrics]:
    """Parse all iteration logs from a run directory."""
    iter_dir = os.path.join(run_dir, "iterations")
    snap_dir = os.path.join(run_dir, "snapshots")

    if not os.path.isdir(iter_dir):
        return []

    iter_files = sorted(
        f for f in os.listdir(iter_dir)
        if re.match(r"^iter_\d+\.json$", f)
    )

    results: list[IterationMetrics] = []
    for fname in iter_files:
        path = os.path.join(iter_dir, fname)
        try:
            with open(path) as f:
                iter_data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        agent = iter_data.get("agent", "unknown")
        parser = get_parser(agent)
        if parser is None:
            # Fallback: extract basic info without parsing stdout
            output = iter_data.get("output", {})
            im = IterationMetrics(
                iteration=iter_data.get("iteration", 0),
                agent=agent,
                model=iter_data.get("model", "unknown"),
                duration_seconds=output.get("duration_seconds", 0.0),
                success=output.get("success", False),
            )
        else:
            im = parser.parse_iteration(iter_data)

        # Attach snapshot commit and timestamp
        im.snapshot_commit, im.snapshot_timestamp = _load_snapshot(snap_dir, im.iteration)
        im.iteration_timestamp = iter_data.get("timestamp")
        results.append(im)

    results.sort(key=lambda m: m.iteration)
    return results


def aggregate(
    run_dir: str,
    benchmarks: list[BenchmarkSnapshot] | None = None,
) -> RunMetrics:
    """Build RunMetrics from a run log directory.

    Args:
        run_dir: Path to logs/runs/{run_id}/
        benchmarks: Pre-loaded benchmark snapshots (or empty list).
    """
    run_id = os.path.basename(os.path.normpath(run_dir))
    iterations = _parse_iterations(run_dir)

    agent = iterations[0].agent if iterations else "unknown"
    model = iterations[0].model if iterations else "unknown"

    total_tokens = 0
    total_tool_calls = 0
    total_commits = 0
    total_commands = 0
    total_command_successes = 0
    total_command_failures = 0
    total_command_timeouts = 0
    total_files_read = 0
    total_files_written = 0
    total_tests_collected = 0
    total_tests_passed = 0
    peak_context_window_used_tokens: int | None = None
    total_workspace_loc_added: int | None = 0
    total_duration = 0.0
    tool_summary: Counter[str] = Counter()

    ws_git_dir = _find_workspace_git_dir(run_id)
    _attach_workspace_loc_added(run_dir, iterations, workspace_git_dir=ws_git_dir)

    for im in iterations:
        total_tokens += im.tokens_total
        total_tool_calls += im.total_tool_calls
        total_commits += im.commit_count
        total_commands += im.command_count
        total_command_successes += im.command_success_count
        total_command_failures += im.command_failure_count
        total_command_timeouts += im.command_timeout_count
        total_files_read += im.files_read_count
        total_files_written += im.files_written_count
        total_tests_collected += im.tests_collected
        total_tests_passed += im.tests_passed
        if im.max_context_window_used_tokens is not None:
            if peak_context_window_used_tokens is None:
                peak_context_window_used_tokens = im.max_context_window_used_tokens
            else:
                peak_context_window_used_tokens = max(
                    peak_context_window_used_tokens,
                    im.max_context_window_used_tokens,
                )
        if im.workspace_loc_added is None:
            total_workspace_loc_added = None
        elif total_workspace_loc_added is not None:
            total_workspace_loc_added += im.workspace_loc_added
        total_duration += im.duration_seconds
        tool_summary.update(im.tool_calls)

    bench_list = benchmarks or []
    link_benchmarks_to_iterations(bench_list, iterations, workspace_git_dir=ws_git_dir)

    return RunMetrics(
        run_id=run_id,
        agent=agent,
        model=model,
        iterations=iterations,
        benchmarks=bench_list,
        total_tokens=total_tokens,
        total_tool_calls=total_tool_calls,
        total_commits=total_commits,
        total_commands=total_commands,
        total_command_successes=total_command_successes,
        total_command_failures=total_command_failures,
        total_command_timeouts=total_command_timeouts,
        total_files_read=total_files_read,
        total_files_written=total_files_written,
        total_tests_collected=total_tests_collected,
        total_tests_passed=total_tests_passed,
        peak_context_window_used_tokens=peak_context_window_used_tokens,
        total_workspace_loc_added=total_workspace_loc_added,
        total_duration_seconds=total_duration,
        tool_call_summary=dict(tool_summary.most_common()),
        warnings=[im.workspace_loc_issue for im in iterations if im.workspace_loc_issue],
    )
