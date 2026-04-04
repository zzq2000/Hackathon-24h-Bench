from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
from typing import Any, Optional

from .core import (
    EnrichedRunSeries,
    MetricsPoint,
    PlotterError,
    RunSeries,
    ScorePoint,
    compute_elapsed_hours,
    load_many_enriched_series,
    load_many_series,
    load_many_series_from_output,
    parse_start_time_from_run_id,
)


# ══════════════════════════════════════════════════════════════════
# Academic style constants (NeurIPS / ICML paper figures)
# ══════════════════════════════════════════════════════════════════

_ACADEMIC_RCPARAMS: dict = {
    # Font
    "font.family":       "serif",
    "font.serif":        ["DejaVu Serif", "Times New Roman", "serif"],
    "mathtext.fontset":  "dejavuserif",
    "font.size":         10,
    # Axes
    "axes.linewidth":    0.6,
    "axes.edgecolor":    "#333333",
    "axes.labelsize":    10,
    "axes.labelcolor":   "#222222",
    "axes.titlesize":    11,
    "axes.titleweight":  "normal",
    "axes.titlepad":     10,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    # Ticks
    "xtick.labelsize":   8.5,
    "ytick.labelsize":   8.5,
    "xtick.color":       "#333333",
    "ytick.color":       "#333333",
    "xtick.direction":   "in",
    "ytick.direction":   "in",
    "xtick.major.size":  3,
    "ytick.major.size":  3,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "xtick.minor.visible": False,
    # Legend
    "legend.fontsize":   8.5,
    "legend.frameon":    False,
    "legend.handlelength": 2.0,
    "legend.columnspacing": 1.0,
    # Grid
    "grid.alpha":        0.3,
    "grid.linewidth":    0.4,
    "grid.color":        "#AAAAAA",
    # Figure
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "figure.dpi":        150,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
    "savefig.pad_inches": 0.08,
    "savefig.facecolor": "white",
}

# Colourblind-safe academic palette (Wong 2011)
_ACADEMIC_PALETTE = [
    "#0072B2",  # strong blue
    "#009E73",  # bluish green
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#8B4513",  # saddle brown
    "#000000",  # black
]

_ACADEMIC_MARKERS = ["o", "s", "D", "^", "v", "P", "X", "*"]

# Agent prefix -> full display name
_AGENT_DISPLAY_NAMES: dict[str, str] = {
    "codex":    "Codex",
    "claude":   "Claude Code",
    "gemini":   "Gemini CLI",
    "kimi":     "Kimi Code",
    "opencode": "OpenCode",
    "qwen":     "Qwen Code",
    "grok":     "Grok CLI",
    "cline":    "Cline",
}


def _format_display_name(codeagent_model: str) -> str:
    """Convert codeagent_model (e.g. 'claude_sonnet-4') to a readable legend label."""
    if codeagent_model == "unknown":
        return "Unknown"
    parts = codeagent_model.split("_", 1)
    agent = parts[0].lower()
    model = parts[1] if len(parts) > 1 else ""
    agent_name = _AGENT_DISPLAY_NAMES.get(agent, agent.capitalize())
    if model and model != "unknown":
        return f"{agent_name} ({model})"
    return agent_name


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="last-brief-plotter",
        description=(
            "Plot score curves from workspace/<system_type>/<run_id>/last_brief "
            "or from exported meta JSON files."
        ),
    )
    parser.add_argument(
        "--system-type",
        required=False,
        help="System type under workspace, e.g. database or message_queue.",
    )
    parser.add_argument(
        "run_ids",
        nargs="*",
        help="One or more run IDs. Supports full run_id or unique suffix.",
    )
    parser.add_argument(
        "--workspace-root",
        default="workspace",
        help="Workspace root directory. Default: ./workspace",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Output PNG path. Default: ./score_trend_<system_type>_<run_id>.png "
            "(or *_multi.png when plotting multiple runs)."
        ),
    )
    parser.add_argument(
        "--title",
        default=None,
        help="Custom chart title.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show chart window after saving.",
    )
    parser.add_argument(
        "--input-json",
        "--input_json",
        nargs="+",
        default=None,
        help=(
            "Load one or more meta JSON files and auto-merge series before plotting. "
            "When set, positional run_ids are not required."
        ),
    )
    parser.add_argument(
        "--output-json",
        "--output_json",
        nargs="?",
        const="",
        default=None,
        help=(
            "Export plotting metadata as JSON. "
            "Use without value to auto-generate meta_<system_type>_<timestamp>.json."
        ),
    )
    parser.add_argument(
        "--test-interval",
        "--test_interval",
        type=float,
        default=900.0,
        help=(
            "Test interval in seconds between iterations. "
            "Used to convert X-axis to elapsed time in hours. Default: 900"
        ),
    )
    parser.add_argument(
        "--max-hours",
        "--max_hours",
        type=float,
        default=None,
        help="Drop score/metrics points whose elapsed time is greater than this many hours.",
    )
    parser.add_argument(
        "--plot-mode",
        "--plot_mode",
        choices=["score", "combined", "metrics"],
        default="score",
        help="Plot mode: score (default), combined (single-run multi-axis), metrics (multi-run comparison).",
    )
    parser.add_argument(
        "--metrics",
        default="tokens,commits,tools,loc",
        help=(
            "Comma-separated metrics to plot. "
            "Options: tokens, commits, tools, loc, cost, steps, commands, cmd_fail, "
            "cmd_timeout, reads, writes, tests, ctx. "
            "Default: tokens,commits,tools,loc"
        ),
    )
    parser.add_argument(
        "--logs-root",
        "--logs_root",
        default="logs/runs",
        help="Root directory for iteration logs. Default: logs/runs",
    )
    parser.add_argument(
        "--output-root",
        "--output_root",
        default="output",
        help="Root directory for benchmark output. Default: output",
    )
    parser.add_argument(
        "--score-source",
        "--score_source",
        choices=["output", "workspace"],
        default="output",
        help=(
            "Where to read score data from. "
            "'output' (default) reads authoritative benchmark results from output/{run_id}/meta.json. "
            "'workspace' reads from workspace last_brief/*.txt (may contain agent self-reported scores)."
        ),
    )
    return parser


def _normalize_system_type(system_type: Optional[str]) -> Optional[str]:
    if system_type is None:
        return None
    normalized = system_type.strip()
    return normalized if normalized else None


def _default_output_path(
    system_type: str,
    series_list: Optional[list[RunSeries | EnrichedRunSeries]] = None,
) -> Path:
    safe_system = system_type.replace("/", "_")
    if series_list and len(series_list) == 1:
        run_label = series_list[0].run_id.replace("/", "_")
    else:
        run_label = "multi"
    return (Path.cwd() / f"score_trend_{safe_system}_{run_label}.png").resolve()


def _resolve_output_path(
    output_value: Optional[str],
    system_type: str,
    series_list: list[RunSeries | EnrichedRunSeries],
) -> Path:
    if output_value:
        return Path(output_value).expanduser().resolve()
    return _default_output_path(system_type, series_list)


def _resolve_output_json_path(output_json_value: str, system_type: str) -> Path:
    if output_json_value:
        return Path(output_json_value).expanduser().resolve()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_system = system_type.replace("/", "_")
    return (Path.cwd() / f"meta_{safe_system}_{timestamp}.json").resolve()


def _assign_model_styles(
    series_list: list[RunSeries] | list[EnrichedRunSeries],
) -> dict[str, dict[str, str]]:
    """Assign color, marker, linestyle, and display_name per model."""
    model_names = sorted({series.codeagent_model for series in series_list})
    styles: dict[str, dict[str, str]] = {}
    for idx, model_name in enumerate(model_names):
        styles[model_name] = {
            "color": _ACADEMIC_PALETTE[idx % len(_ACADEMIC_PALETTE)],
            "marker": _ACADEMIC_MARKERS[idx % len(_ACADEMIC_MARKERS)],
            "linestyle": "-",
            "display_name": _format_display_name(model_name),
        }
    return styles


def _dump_meta_json(
    path: Path,
    system_type: str,
    series_list: list[RunSeries] | list[EnrichedRunSeries],
) -> None:
    has_metrics = any(
        isinstance(s, EnrichedRunSeries) and s.metrics_points
        for s in series_list
    )
    schema_version = 2 if has_metrics else 1

    serialized_series: list[dict[str, Any]] = []
    for series in series_list:
        entry: dict[str, Any] = {
            "run_id": series.run_id,
            "run_dir": str(series.run_dir),
            "codeagent_model": series.codeagent_model,
            "points": [
                {
                    "test_index": point.test_index,
                    "score": point.score,
                    "snapshot_time": point.snapshot_time.isoformat() if point.snapshot_time else None,
                    "source_file": str(point.source_file),
                }
                for point in series.points
            ],
        }
        if has_metrics and isinstance(series, EnrichedRunSeries):
            entry["metrics"] = [
                {
                    "iteration": mp.iteration,
                    "elapsed_hours": mp.elapsed_hours,
                    "raw_timestamp": mp.raw_timestamp.isoformat() if mp.raw_timestamp else None,
                    "cumulative_tokens": mp.cumulative_tokens,
                    "cumulative_steps": mp.cumulative_steps,
                    "cumulative_tool_calls": mp.cumulative_tool_calls,
                    "cumulative_commits": mp.cumulative_commits,
                    "cumulative_loc_added": mp.cumulative_loc_added,
                    "cumulative_commands": mp.cumulative_commands,
                    "cumulative_command_failures": mp.cumulative_command_failures,
                    "cumulative_command_timeouts": mp.cumulative_command_timeouts,
                    "cumulative_files_read": mp.cumulative_files_read,
                    "cumulative_files_written": mp.cumulative_files_written,
                    "cumulative_tests_collected": mp.cumulative_tests_collected,
                    "cumulative_tests_passed": mp.cumulative_tests_passed,
                    "peak_context_window_used_tokens": mp.peak_context_window_used_tokens,
                    "iteration_tokens": mp.iteration_tokens,
                    "iteration_steps": mp.iteration_steps,
                    "iteration_tool_calls": mp.iteration_tool_calls,
                    "iteration_commits": mp.iteration_commits,
                    "iteration_loc_added": mp.iteration_loc_added,
                    "iteration_commands": mp.iteration_commands,
                    "iteration_command_failures": mp.iteration_command_failures,
                    "iteration_command_timeouts": mp.iteration_command_timeouts,
                    "iteration_files_read": mp.iteration_files_read,
                    "iteration_files_written": mp.iteration_files_written,
                    "iteration_tests_collected": mp.iteration_tests_collected,
                    "iteration_tests_passed": mp.iteration_tests_passed,
                    "iteration_max_context_window_used_tokens": mp.iteration_max_context_window_used_tokens,
                    "cumulative_cost_usd": mp.cumulative_cost_usd,
                    "iteration_cost_usd": mp.iteration_cost_usd,
                }
                for mp in series.metrics_points
            ]
        serialized_series.append(entry)

    payload: dict[str, Any] = {
        "schema_version": schema_version,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "system_type": system_type,
        "series": serialized_series,
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _parse_meta_snapshot_time(raw_value: Any, source_path: Path) -> Optional[datetime]:
    if raw_value is None:
        return None
    if not isinstance(raw_value, str):
        raise PlotterError(f"Invalid snapshot_time in meta file: {source_path}")
    try:
        return datetime.fromisoformat(raw_value)
    except ValueError as exc:
        raise PlotterError(f"Invalid snapshot_time '{raw_value}' in meta file: {source_path}") from exc


def _parse_meta_metrics(raw_metrics: list[dict], source_path: Path) -> list[MetricsPoint]:
    """Parse metrics array from v2 meta JSON."""
    result: list[MetricsPoint] = []
    for raw in raw_metrics:
        if not isinstance(raw, dict):
            continue
        raw_ts = raw.get("raw_timestamp")
        ts: Optional[datetime] = None
        if isinstance(raw_ts, str):
            try:
                ts = datetime.fromisoformat(raw_ts)
            except ValueError:
                pass
        result.append(MetricsPoint(
            iteration=int(raw.get("iteration", 0)),
            elapsed_hours=float(raw.get("elapsed_hours", 0.0)),
            raw_timestamp=ts,
            cumulative_tokens=int(raw.get("cumulative_tokens", 0)),
            cumulative_steps=int(raw.get("cumulative_steps", 0)),
            cumulative_tool_calls=int(raw.get("cumulative_tool_calls", 0)),
            cumulative_commits=int(raw.get("cumulative_commits", 0)),
            cumulative_loc_added=int(raw.get("cumulative_loc_added", 0)),
            cumulative_commands=int(raw.get("cumulative_commands", 0)),
            cumulative_command_failures=int(raw.get("cumulative_command_failures", 0)),
            cumulative_command_timeouts=int(raw.get("cumulative_command_timeouts", 0)),
            cumulative_files_read=int(raw.get("cumulative_files_read", 0)),
            cumulative_files_written=int(raw.get("cumulative_files_written", 0)),
            cumulative_tests_collected=int(raw.get("cumulative_tests_collected", 0)),
            cumulative_tests_passed=int(raw.get("cumulative_tests_passed", 0)),
            peak_context_window_used_tokens=int(raw.get("peak_context_window_used_tokens", 0)),
            iteration_tokens=int(raw.get("iteration_tokens", 0)),
            iteration_steps=int(raw.get("iteration_steps", 0)),
            iteration_tool_calls=int(raw.get("iteration_tool_calls", 0)),
            iteration_commits=int(raw.get("iteration_commits", 0)),
            iteration_loc_added=int(raw.get("iteration_loc_added", 0)),
            iteration_commands=int(raw.get("iteration_commands", 0)),
            iteration_command_failures=int(raw.get("iteration_command_failures", 0)),
            iteration_command_timeouts=int(raw.get("iteration_command_timeouts", 0)),
            iteration_files_read=int(raw.get("iteration_files_read", 0)),
            iteration_files_written=int(raw.get("iteration_files_written", 0)),
            iteration_tests_collected=int(raw.get("iteration_tests_collected", 0)),
            iteration_tests_passed=int(raw.get("iteration_tests_passed", 0)),
            iteration_max_context_window_used_tokens=int(raw.get("iteration_max_context_window_used_tokens", 0)),
            cumulative_cost_usd=float(raw.get("cumulative_cost_usd", 0.0)),
            iteration_cost_usd=float(raw.get("iteration_cost_usd", 0.0)),
        ))
    result.sort(key=lambda mp: mp.iteration)
    return result


def _load_one_meta_json(path: Path) -> tuple[list[RunSeries | EnrichedRunSeries], Optional[str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PlotterError(f"Meta JSON not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PlotterError(f"Invalid JSON in meta file: {path}") from exc

    if not isinstance(payload, dict):
        raise PlotterError(f"Meta JSON root must be an object: {path}")

    schema_version = payload.get("schema_version", 1)
    raw_system_type = payload.get("system_type")
    meta_system_type = raw_system_type.strip() if isinstance(raw_system_type, str) else None

    raw_series = payload.get("series")
    if not isinstance(raw_series, list):
        raise PlotterError(f"Meta JSON missing 'series' list: {path}")

    parsed_series: list[RunSeries | EnrichedRunSeries] = []
    for idx, raw_item in enumerate(raw_series):
        if not isinstance(raw_item, dict):
            raise PlotterError(f"Invalid series item #{idx} in meta file: {path}")

        run_id = str(raw_item.get("run_id", "")).strip()
        if not run_id:
            raise PlotterError(f"Missing run_id in series item #{idx} in meta file: {path}")

        model = str(raw_item.get("codeagent_model", "unknown")).strip() or "unknown"
        run_dir_value = raw_item.get("run_dir")
        run_dir = Path(str(run_dir_value)) if run_dir_value else path.parent

        raw_points = raw_item.get("points")
        if not isinstance(raw_points, list):
            raise PlotterError(f"Invalid points in series '{run_id}' in meta file: {path}")

        points: list[ScorePoint] = []
        for point_idx, raw_point in enumerate(raw_points):
            if not isinstance(raw_point, dict):
                raise PlotterError(f"Invalid point #{point_idx} in series '{run_id}' in meta file: {path}")
            try:
                test_index = int(raw_point["test_index"])
                score = float(raw_point["score"])
            except (KeyError, TypeError, ValueError) as exc:
                raise PlotterError(
                    f"Point #{point_idx} in series '{run_id}' must contain numeric test_index and score: {path}"
                ) from exc

            source_file_value = raw_point.get("source_file")
            source_file = Path(str(source_file_value)) if source_file_value else path
            snapshot_time = _parse_meta_snapshot_time(raw_point.get("snapshot_time"), path)
            points.append(
                ScorePoint(
                    test_index=test_index,
                    score=score,
                    snapshot_time=snapshot_time,
                    source_file=source_file,
                )
            )

        points.sort(key=lambda point: point.test_index)
        if not points:
            continue

        # v2: parse metrics if present
        raw_metrics = raw_item.get("metrics")
        if schema_version >= 2 and isinstance(raw_metrics, list):
            metrics_points = _parse_meta_metrics(raw_metrics, path)
            parsed_series.append(
                EnrichedRunSeries(
                    run_id=run_id,
                    run_dir=run_dir,
                    codeagent_model=model,
                    points=points,
                    metrics_points=metrics_points,
                )
            )
        else:
            parsed_series.append(
                RunSeries(
                    run_id=run_id,
                    run_dir=run_dir,
                    codeagent_model=model,
                    points=points,
                )
            )

    if not parsed_series:
        raise PlotterError(f"No valid series in meta file: {path}")
    return parsed_series, meta_system_type


def _merge_series_list(
    series_list: list[RunSeries | EnrichedRunSeries],
) -> list[RunSeries | EnrichedRunSeries]:
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for series in series_list:
        key = (series.run_id, series.codeagent_model)
        if key not in merged:
            merged[key] = {
                "run_dir": series.run_dir,
                "points": {},
                "metrics": {},
                "has_metrics": False,
            }
        point_map: dict[int, ScorePoint] = merged[key]["points"]
        for point in series.points:
            point_map[point.test_index] = point
        if isinstance(series, EnrichedRunSeries) and series.metrics_points:
            merged[key]["has_metrics"] = True
            metrics_map: dict[int, MetricsPoint] = merged[key]["metrics"]
            for mp in series.metrics_points:
                metrics_map[mp.iteration] = mp

    merged_series: list[RunSeries | EnrichedRunSeries] = []
    for (run_id, model), item in sorted(merged.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        merged_points = sorted(item["points"].values(), key=lambda point: point.test_index)
        if not merged_points:
            continue
        if item["has_metrics"]:
            merged_metrics = sorted(item["metrics"].values(), key=lambda mp: mp.iteration)
            merged_series.append(
                EnrichedRunSeries(
                    run_id=run_id,
                    run_dir=item["run_dir"],
                    codeagent_model=model,
                    points=merged_points,
                    metrics_points=merged_metrics,
                )
            )
        else:
            merged_series.append(
                RunSeries(
                    run_id=run_id,
                    run_dir=item["run_dir"],
                    codeagent_model=model,
                    points=merged_points,
                )
            )

    if not merged_series:
        raise PlotterError("No valid series data found after merging meta JSON.")
    return merged_series


def _load_and_merge_input_json(
    paths: list[str],
) -> tuple[list[RunSeries | EnrichedRunSeries], Optional[str]]:
    unique_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for raw_path in paths:
        normalized = raw_path.strip()
        if not normalized:
            continue
        path = Path(normalized).expanduser().resolve()
        if path in seen_paths:
            continue
        seen_paths.add(path)
        unique_paths.append(path)

    if not unique_paths:
        raise PlotterError("No valid --input_json path provided.")

    all_series: list[RunSeries | EnrichedRunSeries] = []
    inferred_system_types: list[str] = []
    for path in unique_paths:
        series_list, maybe_system_type = _load_one_meta_json(path)
        all_series.extend(series_list)
        if maybe_system_type:
            inferred_system_types.append(maybe_system_type)

    unique_system_types = sorted(set(inferred_system_types))
    merged_series = _merge_series_list(all_series)
    if len(unique_system_types) == 1:
        return merged_series, unique_system_types[0]
    if len(unique_system_types) > 1:
        return merged_series, "mixed"
    return merged_series, None


def _apply_max_hours_filter(
    series_list: list[RunSeries | EnrichedRunSeries],
    max_hours: float,
    test_interval_seconds: float,
) -> list[RunSeries | EnrichedRunSeries]:
    filtered_series: list[RunSeries | EnrichedRunSeries] = []
    for series in series_list:
        start_time = parse_start_time_from_run_id(series.run_id)
        elapsed_hours = compute_elapsed_hours(
            series.points,
            test_interval_seconds,
            start_time=start_time,
        )
        filtered_points = [
            point
            for point, elapsed in zip(series.points, elapsed_hours)
            if elapsed <= max_hours
        ]

        if isinstance(series, EnrichedRunSeries):
            filtered_metrics = [
                point for point in series.metrics_points if point.elapsed_hours <= max_hours
            ]
            filtered_series.append(
                EnrichedRunSeries(
                    run_id=series.run_id,
                    run_dir=series.run_dir,
                    codeagent_model=series.codeagent_model,
                    points=filtered_points,
                    metrics_points=filtered_metrics,
                )
            )
        else:
            filtered_series.append(
                RunSeries(
                    run_id=series.run_id,
                    run_dir=series.run_dir,
                    codeagent_model=series.codeagent_model,
                    points=filtered_points,
                )
            )

    return filtered_series


def _plot_series(
    series_list: list[RunSeries],
    output_path: Path,
    title: str,
    show: bool,
    test_interval_seconds: float,
) -> None:
    try:
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator
    except ImportError as exc:
        raise PlotterError("matplotlib is required. Install with: pip install matplotlib") from exc

    plt.rcParams.update(_ACADEMIC_RCPARAMS)
    model_styles = _assign_model_styles(series_list)

    fig, ax = plt.subplots(figsize=(7, 4))
    seen_models: set[str] = set()
    for series in series_list:
        start_time = parse_start_time_from_run_id(series.run_id)
        x_values = compute_elapsed_hours(series.points, test_interval_seconds, start_time=start_time)
        y_values = [point.score for point in series.points]
        # Prepend origin at launch time (t=0, score=0)
        x_values = [0.0] + x_values
        y_values = [0.0] + y_values
        model_name = series.codeagent_model
        style = model_styles.get(model_name, {})
        c = style.get("color", "#555555")
        mk = style.get("marker", "o")
        display = style.get("display_name", model_name)
        label = display if model_name not in seen_models else "_nolegend_"
        seen_models.add(model_name)
        ax.plot(
            x_values, y_values,
            color=c, linestyle="-", linewidth=1.4,
            marker=mk, markersize=2.5,
            markerfacecolor=c, markeredgecolor="white",
            markeredgewidth=0.4,
            label=label, zorder=3, clip_on=False,
        )
        # subtle fill under curve
        ax.fill_between(x_values, 0, y_values, color=c, alpha=0.06, zorder=1)

    ax.set_title(title, fontweight="medium", loc="center")
    ax.set_xlabel("Elapsed Time (hours)")
    ax.set_ylabel("Score (%)")
    # light horizontal grid only
    ax.yaxis.grid(True, linewidth=0.3, alpha=0.4, color="#999999")
    ax.xaxis.grid(False)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=8))
    ax.set_xlim(left=0)

    all_scores = [point.score for series in series_list for point in series.points]
    if all(score >= 0 for score in all_scores) and all(score <= 100 for score in all_scores):
        ax.set_ylim(0, 105)
    elif all(score >= 0 for score in all_scores):
        ax.set_ylim(bottom=0)

    ax.legend(loc="best", borderaxespad=0.4)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)

    if show:
        plt.show()
    plt.close(fig)


# ---------------------------------------------------------------------------
# Metric label / color configuration
# ---------------------------------------------------------------------------

_METRIC_CONFIG: dict[str, dict] = {
    "tokens": {"label": "Cumulative Tokens", "color": "#ff7f0e", "attr": "cumulative_tokens"},
    "steps": {"label": "Cumulative Steps", "color": "#17becf", "attr": "cumulative_steps", "integer": True},
    "commits": {"label": "Cumulative Commits", "color": "#2ca02c", "attr": "cumulative_commits", "integer": True},
    "tools": {"label": "Cumulative Tool Calls", "color": "#d62728", "attr": "cumulative_tool_calls", "integer": True},
    "loc": {"label": "Cumulative Code Lines Changed", "color": "#9467bd", "attr": "cumulative_loc_added", "integer": True},
    "cost": {"label": "Cumulative Cost ($)", "color": "#8c564b", "attr": "cumulative_cost_usd"},
    "commands": {"label": "Cumulative Commands", "color": "#1f77b4", "attr": "cumulative_commands", "integer": True},
    "cmd_fail": {"label": "Cumulative Command Failures", "color": "#7f7f7f", "attr": "cumulative_command_failures", "integer": True},
    "cmd_timeout": {"label": "Cumulative Command Timeouts", "color": "#bcbd22", "attr": "cumulative_command_timeouts", "integer": True},
    "reads": {"label": "Cumulative File Reads", "color": "#4c78a8", "attr": "cumulative_files_read", "integer": True},
    "writes": {"label": "Cumulative File Writes", "color": "#f58518", "attr": "cumulative_files_written", "integer": True},
    "tests": {"label": "Cumulative Tests Passed", "color": "#54a24b", "attr": "cumulative_tests_passed", "integer": True},
    "ctx": {"label": "Peak Context Tokens", "color": "#e45756", "attr": "peak_context_window_used_tokens", "integer": True},
}


def _parse_metrics_arg(raw: str) -> list[str]:
    """Parse comma-separated metrics argument into validated keys."""
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    valid = [k for k in keys if k in _METRIC_CONFIG]
    return valid if valid else list(_METRIC_CONFIG.keys())


def _format_large_number(value: float) -> str:
    """Format large numbers with K/M suffixes."""
    abs_val = abs(value)
    if abs_val >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs_val >= 10_000:
        return f"{value / 1_000:.0f}K"
    if abs_val >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.0f}"


def _compute_adaptive_ylim(values: list[float], include_zero: bool = False) -> tuple[float, float] | None:
    """Compute a readable Y-axis range from plotted values."""
    if not values:
        return None

    ymin = min(values)
    ymax = max(values)

    if include_zero:
        ymin = min(ymin, 0.0)
        ymax = max(ymax, 0.0)

    if ymax == ymin:
        if ymax == 0:
            return (0.0, 1.0)
        pad = max(abs(ymax) * 0.1, 1.0 if abs(ymax) >= 1 else 0.1)
    else:
        pad = (ymax - ymin) * 0.08

    lower = ymin if include_zero and ymin == 0 else ymin - pad
    upper = ymax + pad

    if upper <= lower:
        upper = lower + 1.0

    return (lower, upper)


def _plot_combined(
    enriched: EnrichedRunSeries,
    output_path: Path,
    title: str,
    show: bool,
    test_interval_seconds: float,
    metric_keys: list[str],
) -> None:
    """Plot single-run combined chart: score on left axis, metrics on right axes."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter, MaxNLocator
    except ImportError as exc:
        raise PlotterError("matplotlib is required. Install with: pip install matplotlib") from exc

    plt.rcParams.update(_ACADEMIC_RCPARAMS)

    n_extra = len(metric_keys) if enriched.metrics_points else 0
    # Reserve right margin: each extra axis beyond the first needs space
    right_margin = 0.06 + max(0, n_extra - 1) * 0.065
    fig_width = 14 + max(0, n_extra - 2) * 1.8  # widen figure for many axes
    fig, ax = plt.subplots(figsize=(fig_width, 7))

    # Re-enable right spine for twin axes
    ax.spines["right"].set_visible(True)

    display_name = _format_display_name(enriched.codeagent_model)

    # --- Score curve (left Y axis) ---
    start_time = parse_start_time_from_run_id(enriched.run_id)
    x_score = compute_elapsed_hours(enriched.points, test_interval_seconds, start_time=start_time)
    y_score = [p.score for p in enriched.points]
    # Prepend origin at launch time
    x_score = [0.0] + x_score
    y_score = [0.0] + y_score
    score_line, = ax.plot(
        x_score, y_score,
        marker="o", markersize=3.5, markevery=5,
        markerfacecolor="#0072B2", markeredgecolor="white",
        markeredgewidth=0.6,
        linewidth=1.4, color="#0072B2",
        label=f"{display_name} Score (%)",
    )
    ax.fill_between(x_score, 0, y_score, color="#0072B2", alpha=0.06, zorder=1)
    ax.set_xlabel("Elapsed Time (hours)")
    ax.set_ylabel("Score (%)", color="#0072B2")
    ax.tick_params(axis="y", labelcolor="#0072B2")
    all_scores = [p.score for p in enriched.points]
    if all(0 <= s <= 100 for s in all_scores):
        ax.set_ylim(0, 105)
    else:
        ax.set_ylim(bottom=0)
    ax.yaxis.grid(True, linewidth=0.3, alpha=0.4, color="#999999")
    ax.xaxis.grid(False)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=8))
    ax.set_xlim(left=0)

    # --- Metric curves (right Y axes) ---
    lines = [score_line]
    labels = [f"{display_name} Score (%)"]
    axes_extra: list = []

    if enriched.metrics_points:
        x_metrics = [0.0] + [mp.elapsed_hours for mp in enriched.metrics_points]
        axis_offset = 0.12  # spacing between stacked right axes

        for i, key in enumerate(metric_keys):
            cfg = _METRIC_CONFIG[key]
            y_vals = [0] + [getattr(mp, cfg["attr"]) for mp in enriched.metrics_points]
            twin = ax.twinx()
            twin.spines["top"].set_visible(False)
            twin.spines["right"].set_visible(True)
            if i > 0:
                twin.spines["right"].set_position(("axes", 1.0 + axis_offset * i))
            twin.set_ylabel(cfg["label"], color=cfg["color"], fontsize=9, labelpad=3)
            twin.tick_params(axis="y", labelcolor=cfg["color"], labelsize=8, pad=2)
            if cfg.get("integer"):
                twin.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))
            else:
                twin.yaxis.set_major_locator(MaxNLocator(nbins=6))
            twin.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _format_large_number(v)))
            line, = twin.plot(x_metrics, y_vals, linestyle="--", linewidth=1.2, color=cfg["color"], label=cfg["label"])
            ylim = _compute_adaptive_ylim(y_vals, include_zero=True)
            if ylim is not None:
                twin.set_ylim(*ylim)
            lines.append(line)
            labels.append(cfg["label"])
            axes_extra.append(twin)

    ax.legend(lines, labels, loc="upper left", borderaxespad=0.4)
    ax.set_title(title or f"Combined: {display_name}", fontweight="medium")
    fig.tight_layout()
    # Adjust right margin after tight_layout to make room for extra y-axes
    if n_extra > 1:
        fig.subplots_adjust(right=1.0 - right_margin)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)

    if show:
        plt.show()
    plt.close(fig)


def _plot_metrics_comparison(
    enriched_list: list[EnrichedRunSeries],
    output_path: Path,
    title: str,
    show: bool,
    test_interval_seconds: float,
    metric_keys: list[str],
) -> None:
    """Plot multi-run metrics comparison with one subplot per metric."""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter, MaxNLocator
    except ImportError as exc:
        raise PlotterError("matplotlib is required. Install with: pip install matplotlib") from exc

    plt.rcParams.update(_ACADEMIC_RCPARAMS)

    n_metrics = len(metric_keys)
    if n_metrics == 0:
        raise PlotterError("No valid metrics to plot.")

    model_styles = _assign_model_styles(enriched_list)

    fig, axes = plt.subplots(nrows=n_metrics, figsize=(10, 4 * n_metrics), sharex=True, squeeze=False)

    for row, key in enumerate(metric_keys):
        cfg = _METRIC_CONFIG[key]
        ax = axes[row, 0]
        seen_models: set[str] = set()
        subplot_values: list[float] = []

        for series in enriched_list:
            if not series.metrics_points:
                continue
            x_vals = [0.0] + [mp.elapsed_hours for mp in series.metrics_points]
            y_vals = [0] + [getattr(mp, cfg["attr"]) for mp in series.metrics_points]
            subplot_values.extend(y_vals)
            model_name = series.codeagent_model
            style = model_styles.get(model_name, {})
            c = style.get("color", "#555555")
            mk = style.get("marker", "o")
            display = style.get("display_name", model_name)
            label = display if model_name not in seen_models else "_nolegend_"
            seen_models.add(model_name)
            ax.plot(
                x_vals, y_vals,
                color=c, linewidth=1.3,
                marker=mk, markersize=3, markevery=5,
                markerfacecolor=c, markeredgecolor="white",
                markeredgewidth=0.5,
                label=label, zorder=3,
            )

        ax.set_ylabel(cfg["label"])
        if cfg.get("integer"):
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _format_large_number(v)))
        ax.yaxis.grid(True, linewidth=0.3, alpha=0.4, color="#999999")
        ax.xaxis.grid(False)
        ax.set_xlim(left=0)
        ylim = _compute_adaptive_ylim(subplot_values, include_zero=True)
        if ylim is not None:
            ax.set_ylim(*ylim)
        ax.legend(loc="best", borderaxespad=0.4)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=8))

    axes[-1, 0].set_xlabel("Elapsed Time (hours)")
    fig.suptitle(title or "Metrics Comparison", fontsize=12, fontweight="medium")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)

    if show:
        plt.show()
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.test_interval <= 0:
        parser.error("--test-interval/--test_interval must be positive.")
    if args.max_hours is not None and args.max_hours < 0:
        parser.error("--max-hours/--max_hours must be non-negative.")

    arg_system_type = _normalize_system_type(args.system_type)
    plot_mode: str = args.plot_mode
    metric_keys = _parse_metrics_arg(args.metrics)
    score_source: str = args.score_source

    try:
        if args.input_json:
            if args.run_ids:
                parser.error("run_ids cannot be used with --input_json/--input-json.")
            series_list, inferred_system_type = _load_and_merge_input_json(args.input_json)
            system_type = arg_system_type or inferred_system_type or "meta"
        else:
            if arg_system_type is None:
                parser.error("--system-type is required unless --input_json/--input-json is provided.")
            if not args.run_ids:
                parser.error("run_ids are required unless --input_json/--input-json is provided.")
            system_type = arg_system_type
            series_list = None  # loaded lazily below

        workspace_root = Path(args.workspace_root).expanduser().resolve()
        title = args.title or f"Score Trend by Run ({system_type})"

        if plot_mode == "score":
            if series_list is None:
                if score_source == "output":
                    series_list = load_many_series_from_output(
                        workspace_root=workspace_root,
                        system_type=system_type,
                        run_ids=args.run_ids,
                        output_root=args.output_root,
                    )
                else:
                    series_list = load_many_series(
                        workspace_root=workspace_root,
                        system_type=system_type,
                        run_ids=args.run_ids,
                    )
            if args.max_hours is not None:
                series_list = _apply_max_hours_filter(
                    series_list,
                    args.max_hours,
                    args.test_interval,
                )
            if not any(series.points for series in series_list):
                raise PlotterError("No score points remain after applying --max-hours.")
            output_path = _resolve_output_path(args.output, system_type, series_list)
            _plot_series(
                series_list=series_list,
                output_path=output_path,
                title=title,
                show=args.show,
                test_interval_seconds=args.test_interval,
            )
            if args.output_json is not None:
                meta_output_path = _resolve_output_json_path(args.output_json, system_type)
                _dump_meta_json(meta_output_path, system_type, series_list)
                print(f"Saved meta json: {meta_output_path}")

        elif plot_mode == "combined":
            if args.input_json:
                # From JSON: use first EnrichedRunSeries (or wrap RunSeries)
                enriched_candidates = [
                    s for s in series_list if isinstance(s, EnrichedRunSeries)
                ]
                if not enriched_candidates:
                    # Wrap plain RunSeries as EnrichedRunSeries with empty metrics
                    s0 = series_list[0]
                    enriched = EnrichedRunSeries(
                        run_id=s0.run_id, run_dir=s0.run_dir,
                        codeagent_model=s0.codeagent_model, points=s0.points,
                    )
                else:
                    enriched = enriched_candidates[0]
            else:
                run_ids = args.run_ids or []
                if len(run_ids) != 1:
                    parser.error("--plot-mode combined requires exactly one run_id.")
                enriched = load_many_enriched_series(
                    workspace_root=workspace_root,
                    system_type=system_type,
                    run_ids=run_ids,
                    logs_root=args.logs_root,
                    output_root=args.output_root,
                    score_source=score_source,
                )[0]
            if args.max_hours is not None:
                enriched = _apply_max_hours_filter(
                    [enriched],
                    args.max_hours,
                    args.test_interval,
                )[0]
            if not enriched.points and not enriched.metrics_points:
                raise PlotterError("No data points remain after applying --max-hours.")
            output_path = _resolve_output_path(args.output, system_type, [enriched])
            _plot_combined(
                enriched=enriched,
                output_path=output_path,
                title=title,
                show=args.show,
                test_interval_seconds=args.test_interval,
                metric_keys=metric_keys,
            )
            if args.output_json is not None:
                meta_output_path = _resolve_output_json_path(args.output_json, system_type)
                _dump_meta_json(meta_output_path, system_type, [enriched])
                print(f"Saved meta json: {meta_output_path}")

        elif plot_mode == "metrics":
            if args.input_json:
                # From JSON: use all EnrichedRunSeries from loaded data
                enriched_list = [
                    s if isinstance(s, EnrichedRunSeries)
                    else EnrichedRunSeries(
                        run_id=s.run_id, run_dir=s.run_dir,
                        codeagent_model=s.codeagent_model, points=s.points,
                    )
                    for s in series_list
                ]
            else:
                enriched_list = load_many_enriched_series(
                    workspace_root=workspace_root,
                    system_type=system_type,
                    run_ids=args.run_ids,
                    logs_root=args.logs_root,
                    output_root=args.output_root,
                    score_source=score_source,
                )
            if args.max_hours is not None:
                enriched_list = _apply_max_hours_filter(
                    enriched_list,
                    args.max_hours,
                    args.test_interval,
                )
            if not any(series.metrics_points for series in enriched_list):
                raise PlotterError("No metrics points remain after applying --max-hours.")
            output_path = _resolve_output_path(args.output, system_type, enriched_list)
            _plot_metrics_comparison(
                enriched_list=enriched_list,
                output_path=output_path,
                title=title,
                show=args.show,
                test_interval_seconds=args.test_interval,
                metric_keys=metric_keys,
            )
            if args.output_json is not None:
                meta_output_path = _resolve_output_json_path(args.output_json, system_type)
                _dump_meta_json(meta_output_path, system_type, enriched_list)
                print(f"Saved meta json: {meta_output_path}")

    except PlotterError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved plot: {output_path}")
    return 0
