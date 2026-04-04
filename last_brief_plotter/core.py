from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re
from typing import Iterable, Optional

from metrics.benchmark_linker import resolve_iteration_local_time

logger = logging.getLogger(__name__)


_RUN_ID_TIMESTAMP_RE = re.compile(r"_(\d{8}_\d{6})$")
FILE_INDEX_PATTERN = re.compile(r"last[_-]brief_(\d+)\.txt$", re.IGNORECASE)
SNAPSHOT_TIME_PATTERN = re.compile(r"^\s*snapshot_time:\s*(.+?)\s*$", re.MULTILINE)
SCORE_LINE_PATTERN = re.compile(r"^\s*score:\s*(.+?)\s*$", re.MULTILINE)
SCORE_PERCENT_PATTERN = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s*%")
SCORE_RATIO_PATTERN = re.compile(r"(\d+)\s*/\s*(\d+)")
SCORE_NUMBER_PATTERN = re.compile(r"^([0-9]+(?:\.[0-9]+)?)$")


class PlotterError(Exception):
    """Raised when the input data is invalid or missing."""


@dataclass(frozen=True)
class ScorePoint:
    test_index: int
    score: float
    snapshot_time: Optional[datetime]
    source_file: Path


@dataclass(frozen=True)
class RunSeries:
    run_id: str
    run_dir: Path
    codeagent_model: str
    points: list[ScorePoint]


@dataclass(frozen=True)
class MetricsPoint:
    iteration: int
    elapsed_hours: float
    raw_timestamp: Optional[datetime]
    cumulative_tokens: int
    cumulative_steps: int
    cumulative_tool_calls: int
    cumulative_commits: int
    cumulative_loc_added: int
    iteration_tokens: int = 0
    iteration_steps: int = 0
    iteration_tool_calls: int = 0
    iteration_commits: int = 0
    iteration_loc_added: int = 0
    cumulative_commands: int = 0
    cumulative_command_failures: int = 0
    cumulative_command_timeouts: int = 0
    cumulative_files_read: int = 0
    cumulative_files_written: int = 0
    cumulative_tests_collected: int = 0
    cumulative_tests_passed: int = 0
    peak_context_window_used_tokens: int = 0
    iteration_commands: int = 0
    iteration_command_failures: int = 0
    iteration_command_timeouts: int = 0
    iteration_files_read: int = 0
    iteration_files_written: int = 0
    iteration_tests_collected: int = 0
    iteration_tests_passed: int = 0
    iteration_max_context_window_used_tokens: int = 0
    cumulative_cost_usd: float = 0.0
    iteration_cost_usd: float = 0.0


@dataclass(frozen=True)
class EnrichedRunSeries:
    run_id: str
    run_dir: Path
    codeagent_model: str
    points: list[ScorePoint]
    metrics_points: list[MetricsPoint] = field(default_factory=list)


@dataclass(frozen=True)
class ParsedBriefRecord:
    file_path: Path
    file_index: Optional[int]
    snapshot_time: Optional[datetime]
    score: float


def parse_codeagent_model(run_id: str, system_type: str) -> str:
    normalized_system_type = system_type.strip().strip("_")
    if not normalized_system_type:
        return "unknown"

    prefix = f"{normalized_system_type}_"
    if not run_id.startswith(prefix):
        return "unknown"

    timestamp_match = _RUN_ID_TIMESTAMP_RE.search(run_id)
    if not timestamp_match:
        return "unknown"

    agent_model = run_id[len(prefix):timestamp_match.start()]
    agent, separator, model = agent_model.partition("_")
    if not agent or separator != "_" or not model:
        return "unknown"

    return f"{agent}_{model}"


def parse_start_time_from_run_id(run_id: str) -> Optional[datetime]:
    """Extract the launch timestamp from a run_id's trailing YYYYMMDD_HHMMSS."""
    m = _RUN_ID_TIMESTAMP_RE.search(run_id)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def resolve_run_dir(workspace_root: Path, system_type: str, run_id: str) -> Path:
    system_dir = workspace_root / system_type
    if not system_dir.is_dir():
        raise PlotterError(f"System directory does not exist: {system_dir}")

    exact = system_dir / run_id
    if exact.is_dir():
        return exact

    all_dirs = [path for path in system_dir.iterdir() if path.is_dir()]
    suffix_matches = [path for path in all_dirs if path.name.endswith(run_id)]
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if len(suffix_matches) > 1:
        names = ", ".join(path.name for path in suffix_matches)
        raise PlotterError(f"Run ID '{run_id}' is ambiguous; suffix matches: {names}")

    contains_matches = [path for path in all_dirs if run_id in path.name]
    if len(contains_matches) == 1:
        return contains_matches[0]
    if len(contains_matches) > 1:
        names = ", ".join(path.name for path in contains_matches)
        raise PlotterError(f"Run ID '{run_id}' is ambiguous; contains matches: {names}")

    raise PlotterError(f"Run ID '{run_id}' was not found under: {system_dir}")


def _resolve_last_brief_dir(run_dir: Path) -> Path:
    for candidate in ("last_brief", "last-brief"):
        path = run_dir / candidate
        if path.is_dir():
            return path
    raise PlotterError(f"No last_brief/last-brief directory under run: {run_dir}")


def _extract_file_index(path: Path) -> Optional[int]:
    match = FILE_INDEX_PATTERN.search(path.name)
    if match:
        return int(match.group(1))
    return None


def _parse_snapshot_time(text: str) -> Optional[datetime]:
    match = SNAPSHOT_TIME_PATTERN.search(text)
    if not match:
        return None
    raw = match.group(1).strip()
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _parse_score(score_line: str) -> Optional[float]:
    percent_match = SCORE_PERCENT_PATTERN.search(score_line)
    if percent_match:
        return float(percent_match.group(1))

    ratio_match = SCORE_RATIO_PATTERN.search(score_line)
    if ratio_match:
        numerator = int(ratio_match.group(1))
        denominator = int(ratio_match.group(2))
        if denominator == 0:
            return None
        return numerator / denominator * 100.0

    number_match = SCORE_NUMBER_PATTERN.search(score_line.strip())
    if number_match:
        return float(number_match.group(1))

    return None


def _parse_brief_file(path: Path) -> Optional[ParsedBriefRecord]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    score_line_match = SCORE_LINE_PATTERN.search(text)
    if not score_line_match:
        return None

    score = _parse_score(score_line_match.group(1))
    if score is None:
        return None

    return ParsedBriefRecord(
        file_path=path,
        file_index=_extract_file_index(path),
        snapshot_time=_parse_snapshot_time(text),
        score=score,
    )


def _build_points(records: list[ParsedBriefRecord]) -> list[ScorePoint]:
    if not records:
        return []

    indices = [record.file_index for record in records]
    use_file_indices = all(index is not None for index in indices) and len(set(indices)) == len(records)

    if use_file_indices:
        indexed_records = [record for record in records if record.file_index is not None]
        indexed_records.sort(key=lambda record: record.file_index)
        return [
            ScorePoint(
                test_index=record.file_index,
                score=record.score,
                snapshot_time=record.snapshot_time,
                source_file=record.file_path,
            )
            for record in indexed_records
        ]

    records.sort(
        key=lambda record: (
            record.snapshot_time is None,
            record.snapshot_time or datetime.min,
            record.file_path.name,
        )
    )
    points: list[ScorePoint] = []
    for idx, record in enumerate(records, start=1):
        points.append(
            ScorePoint(
                test_index=idx,
                score=record.score,
                snapshot_time=record.snapshot_time,
                source_file=record.file_path,
            )
        )
    return points


def load_run_series(workspace_root: Path, system_type: str, run_id: str) -> RunSeries:
    run_dir = resolve_run_dir(workspace_root, system_type, run_id)
    last_brief_dir = _resolve_last_brief_dir(run_dir)

    parsed_records: list[ParsedBriefRecord] = []
    for path in last_brief_dir.glob("*.txt"):
        parsed = _parse_brief_file(path)
        if parsed is not None:
            parsed_records.append(parsed)

    points = _build_points(parsed_records)
    if not points:
        raise PlotterError(f"No valid score data in: {last_brief_dir}")

    return RunSeries(
        run_id=run_dir.name,
        run_dir=run_dir,
        codeagent_model=parse_codeagent_model(run_dir.name, system_type),
        points=points,
    )


def _find_output_run_dir(run_id: str, output_root: str = "output") -> Optional[Path]:
    """Find the output/{run_id} directory, trying exact match and suffix/contains fallback."""
    candidate = Path(output_root) / run_id
    if candidate.is_dir():
        return candidate

    root = Path(output_root)
    if not root.is_dir():
        return None

    all_dirs = [d for d in root.iterdir() if d.is_dir()]
    suffix_matches = [d for d in all_dirs if d.name.endswith(run_id)]
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    contains_matches = [d for d in all_dirs if run_id in d.name]
    if len(contains_matches) == 1:
        return contains_matches[0]
    return None


_OUTPUT_DIR_RE = re.compile(r"^output_(\d+)$")


def load_run_series_from_output(
    workspace_root: Path,
    system_type: str,
    run_id: str,
    output_root: str = "output",
) -> RunSeries:
    """Load a RunSeries from output/{run_id}/output_N/meta.json (authoritative benchmark results).

    Falls back to workspace last_brief if the output directory is not found.
    """
    # Resolve run_dir from workspace (needed for run_dir field and codeagent_model)
    run_dir = resolve_run_dir(workspace_root, system_type, run_id)
    resolved_run_id = run_dir.name

    output_dir = _find_output_run_dir(resolved_run_id, output_root)
    if output_dir is None:
        logger.debug("No output dir for %s, falling back to last_brief", resolved_run_id)
        return load_run_series(workspace_root, system_type, run_id)

    points: list[ScorePoint] = []
    for entry in sorted(output_dir.iterdir()):
        m = _OUTPUT_DIR_RE.match(entry.name)
        if not m:
            continue
        meta_path = entry / "meta.json"
        if not meta_path.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        test_index = meta.get("test_index", int(m.group(1)))
        score = float(meta.get("score", 0.0))
        raw_snapshot = meta.get("snapshot_time")
        snapshot_time: Optional[datetime] = None
        if isinstance(raw_snapshot, str):
            try:
                snapshot_time = datetime.fromisoformat(raw_snapshot)
            except ValueError:
                pass

        points.append(ScorePoint(
            test_index=test_index,
            score=score,
            snapshot_time=snapshot_time,
            source_file=meta_path,
        ))

    points.sort(key=lambda p: p.test_index)

    if not points:
        logger.debug("No output meta.json for %s, falling back to last_brief", resolved_run_id)
        return load_run_series(workspace_root, system_type, run_id)

    return RunSeries(
        run_id=resolved_run_id,
        run_dir=run_dir,
        codeagent_model=parse_codeagent_model(resolved_run_id, system_type),
        points=points,
    )


def load_many_series_from_output(
    workspace_root: Path,
    system_type: str,
    run_ids: Iterable[str],
    output_root: str = "output",
) -> list[RunSeries]:
    """Load multiple RunSeries from output directory."""
    unique_run_ids: list[str] = []
    seen: set[str] = set()
    for run_id in run_ids:
        normalized = run_id.strip()
        if not normalized or normalized in seen:
            continue
        unique_run_ids.append(normalized)
        seen.add(normalized)

    if not unique_run_ids:
        raise PlotterError("No valid run_id provided.")

    return [
        load_run_series_from_output(workspace_root, system_type, rid, output_root)
        for rid in unique_run_ids
    ]


def load_many_series(workspace_root: Path, system_type: str, run_ids: Iterable[str]) -> list[RunSeries]:
    unique_run_ids = []
    seen = set()
    for run_id in run_ids:
        normalized = run_id.strip()
        if not normalized or normalized in seen:
            continue
        unique_run_ids.append(normalized)
        seen.add(normalized)

    if not unique_run_ids:
        raise PlotterError("No valid run_id provided.")

    all_series: list[RunSeries] = []
    for run_id in unique_run_ids:
        all_series.append(load_run_series(workspace_root, system_type, run_id))
    return all_series


def compute_elapsed_hours(
    points: list[ScorePoint],
    fallback_interval_sec: float = 900.0,
    start_time: Optional[datetime] = None,
) -> list[float]:
    """Compute elapsed hours for each point, using real snapshot_time when available.

    When *start_time* is provided and all points have a snapshot_time, hours
    are measured from *start_time* (the system launch time).  Otherwise falls
    back to the earliest snapshot_time as T=0, or to synthetic time based on
    test_index offsets.
    """
    if not points:
        return []

    snapshot_times = [p.snapshot_time for p in points]
    if all(t is not None for t in snapshot_times):
        t0 = start_time if start_time is not None else min(snapshot_times)  # type: ignore[arg-type]
        return [max(0.0, (t - t0).total_seconds() / 3600.0) for t in snapshot_times]  # type: ignore[union-attr]
    first_idx = min(p.test_index for p in points)
    return [(p.test_index - first_idx) * fallback_interval_sec / 3600.0 for p in points]


def _parse_timestamp(raw: str | None) -> Optional[datetime]:
    """Try to parse an ISO-format timestamp string."""
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def _build_cumulative_metrics(
    iterations: list,  # list[IterationMetrics]
    start_time: Optional[datetime] = None,
    workspace_git_dir: str | None = None,
) -> list[MetricsPoint]:
    """Build cumulative MetricsPoint list from IterationMetrics.

    When ``start_time`` is available, the metrics X-axis is anchored to the
    run launch time so combined plots share the same T0 as score points.
    """
    if not iterations:
        return []

    cum_tokens = 0
    cum_steps = 0
    cum_tool_calls = 0
    cum_commits = 0
    cum_loc = 0
    cum_commands = 0
    cum_command_failures = 0
    cum_command_timeouts = 0
    cum_files_read = 0
    cum_files_written = 0
    cum_tests_collected = 0
    cum_tests_passed = 0
    peak_context_window_used_tokens = 0
    cum_cost = 0.0
    result: list[MetricsPoint] = []

    # Find T0 from the earliest available timestamp
    raw_times: list[Optional[datetime]] = []
    for im in iterations:
        ts = _parse_timestamp(resolve_iteration_local_time(im, workspace_git_dir=workspace_git_dir))
        raw_times.append(ts)

    valid_times = [t for t in raw_times if t is not None]
    t0 = start_time if start_time is not None else (min(valid_times) if valid_times else None)

    for im, raw_ts in zip(iterations, raw_times):
        loc_added = 0 if im.workspace_loc_added is None else im.workspace_loc_added
        cum_tokens += im.tokens_total
        cum_steps += im.step_count
        cum_tool_calls += im.total_tool_calls
        cum_commits += im.commit_count
        cum_loc += loc_added
        cum_commands += im.command_count
        cum_command_failures += im.command_failure_count
        cum_command_timeouts += im.command_timeout_count
        cum_files_read += im.files_read_count
        cum_files_written += im.files_written_count
        cum_tests_collected += im.tests_collected
        cum_tests_passed += im.tests_passed
        iter_context = im.max_context_window_used_tokens or 0
        peak_context_window_used_tokens = max(peak_context_window_used_tokens, iter_context)
        iter_cost = im.cost_usd if im.cost_usd is not None else 0.0
        cum_cost += iter_cost

        if t0 is not None and raw_ts is not None:
            # Clamp at zero to keep plots anchored at the origin under minor
            # clock skew or imperfect fallback timestamps.
            elapsed = max(0.0, (raw_ts - t0).total_seconds() / 3600.0)
        else:
            elapsed = 0.0

        result.append(MetricsPoint(
            iteration=im.iteration,
            elapsed_hours=elapsed,
            raw_timestamp=raw_ts,
            cumulative_tokens=cum_tokens,
            cumulative_steps=cum_steps,
            cumulative_tool_calls=cum_tool_calls,
            cumulative_commits=cum_commits,
            cumulative_loc_added=cum_loc,
            iteration_tokens=im.tokens_total,
            iteration_steps=im.step_count,
            iteration_tool_calls=im.total_tool_calls,
            iteration_commits=im.commit_count,
            iteration_loc_added=loc_added,
            cumulative_commands=cum_commands,
            cumulative_command_failures=cum_command_failures,
            cumulative_command_timeouts=cum_command_timeouts,
            cumulative_files_read=cum_files_read,
            cumulative_files_written=cum_files_written,
            cumulative_tests_collected=cum_tests_collected,
            cumulative_tests_passed=cum_tests_passed,
            peak_context_window_used_tokens=peak_context_window_used_tokens,
            iteration_commands=im.command_count,
            iteration_command_failures=im.command_failure_count,
            iteration_command_timeouts=im.command_timeout_count,
            iteration_files_read=im.files_read_count,
            iteration_files_written=im.files_written_count,
            iteration_tests_collected=im.tests_collected,
            iteration_tests_passed=im.tests_passed,
            iteration_max_context_window_used_tokens=iter_context,
            cumulative_cost_usd=cum_cost,
            iteration_cost_usd=iter_cost,
        ))
    return result


def _find_logs_run_dir(run_id: str, logs_root: str = "logs/runs") -> Optional[Path]:
    """Find the logs/runs/{run_id} directory, trying with and without system_type prefix."""
    candidate = Path(logs_root) / run_id
    if candidate.is_dir():
        return candidate

    # Try without system_type prefix (e.g. "database_gemini_..." -> "gemini_...")
    parts = run_id.split("_", 1)
    if len(parts) == 2:
        short_id = parts[1]
        candidate = Path(logs_root) / short_id
        if candidate.is_dir():
            return candidate

    # Try scanning logs_root for directories that end with or contain run_id
    logs_path = Path(logs_root)
    if logs_path.is_dir():
        for d in logs_path.iterdir():
            if d.is_dir() and (d.name.endswith(run_id) or run_id.endswith(d.name)):
                return d

    return None


def load_enriched_run_series(
    workspace_root: Path,
    system_type: str,
    run_id: str,
    logs_root: str = "logs/runs",
    output_root: str = "output",
    score_source: str = "output",
) -> EnrichedRunSeries:
    """Load a RunSeries enriched with iteration metrics data.

    Args:
        score_source: "output" (default, authoritative benchmark results from
            output/{run_id}/meta.json) or "workspace" (legacy last_brief parsing).
    """
    if score_source == "output":
        base_series = load_run_series_from_output(workspace_root, system_type, run_id, output_root)
    else:
        base_series = load_run_series(workspace_root, system_type, run_id)
    resolved_run_id = base_series.run_id

    logs_dir = _find_logs_run_dir(resolved_run_id, logs_root)
    metrics_points: list[MetricsPoint] = []

    if logs_dir is not None:
        try:
            from metrics.aggregator import aggregate
            from metrics.benchmark_linker import load_benchmarks

            bench_dir = os.path.join(output_root, resolved_run_id)
            benchmarks = load_benchmarks(bench_dir)
            run_metrics = aggregate(str(logs_dir), benchmarks)
            start_time = parse_start_time_from_run_id(base_series.run_id)
            workspace_git_dir = str(base_series.run_dir) if (base_series.run_dir / ".git").is_dir() else None
            metrics_points = _build_cumulative_metrics(
                run_metrics.iterations,
                start_time=start_time,
                workspace_git_dir=workspace_git_dir,
            )
        except Exception:
            logger.debug("Failed to load metrics for %s, using empty metrics", resolved_run_id, exc_info=True)

    return EnrichedRunSeries(
        run_id=base_series.run_id,
        run_dir=base_series.run_dir,
        codeagent_model=base_series.codeagent_model,
        points=base_series.points,
        metrics_points=metrics_points,
    )


def load_many_enriched_series(
    workspace_root: Path,
    system_type: str,
    run_ids: Iterable[str],
    logs_root: str = "logs/runs",
    output_root: str = "output",
    score_source: str = "output",
) -> list[EnrichedRunSeries]:
    """Load multiple enriched run series."""
    unique_run_ids: list[str] = []
    seen: set[str] = set()
    for run_id in run_ids:
        normalized = run_id.strip()
        if not normalized or normalized in seen:
            continue
        unique_run_ids.append(normalized)
        seen.add(normalized)

    if not unique_run_ids:
        raise PlotterError("No valid run_id provided.")

    return [
        load_enriched_run_series(
            workspace_root, system_type, rid, logs_root, output_root, score_source,
        )
        for rid in unique_run_ids
    ]
