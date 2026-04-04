# last_brief_plotter

Plot score trends and iteration metrics for benchmark runs.

By default, scores are read from the authoritative benchmark results in `output/<run_id>/output_N/meta.json`. Use `--score-source workspace` to fall back to parsing `workspace/<system_type>/<run_id>/last_brief/*.txt` (which may contain agent self-reported scores).

## Plot Modes

### Score mode (default)

Score trend over time. Supports multiple runs for comparison.

```bash
python3 -m last_brief_plotter --system-type database <run_id_1> <run_id_2>
```

### Combined mode

Single-run multi-axis chart: score (left Y) + selected cumulative metrics (right Y axes). By default it plots `tokens,commits,tools,loc`; `cost` and `steps` can be enabled via `--metrics`. Requires iteration logs in `logs/runs/<run_id>/`.

```bash
python3 -m last_brief_plotter --system-type database --plot-mode combined <run_id>
```

### Metrics mode

Multi-run comparison with one subplot per metric (tokens, commits, tools, LOC, cost, steps). Each subplot overlays all runs with per-run relative time (T=0).

```bash
python3 -m last_brief_plotter --system-type database --plot-mode metrics <run_id_1> <run_id_2>
```

## Usage Examples

Basic score plot:

```bash
python3 -m last_brief_plotter --system-type database \
  database_gemini_gemini-3-pro-preview_20260220_123422
```

Combined plot with specific metrics:

```bash
python3 -m last_brief_plotter --system-type database \
  --plot-mode combined \
  --max-hours 24 \
  --metrics tokens,loc \
  --output ./plots/combined.png \
  database_opencode_bailian-coding-plan-qwen3.5-plus_20260302_182727
```

Metrics comparison across runs:

```bash
python3 -m last_brief_plotter --system-type database \
  --plot-mode metrics \
  --output ./plots/metrics_cmp.png \
  database_opencode_bailian-coding-plan-qwen3.5-plus_20260302_182727 \
  database_opencode_bailian-coding-plan-glm-5_20260303_111905
```

Export and re-import meta JSON:

```bash
# Export (v2 schema includes metrics when available)
python3 -m last_brief_plotter --system-type database \
  --plot-mode combined --output_json \
  database_opencode_bailian-coding-plan-qwen3.5-plus_20260302_182727

# Re-import and plot from meta JSON
python3 -m last_brief_plotter \
  --input_json ./meta_database_20260303_120000.json \
  --output ./plots/from_meta.png
```

Use legacy workspace last_brief as score source:

```bash
python3 -m last_brief_plotter --system-type database \
  --score-source workspace \
  database_gemini_gemini-3-pro-preview_20260220_123422
```

Unique run-id suffix also works:

```bash
python3 -m last_brief_plotter --system-type database 20260219_114706
```

## CLI Reference

| Argument | Default | Description |
|----------|---------|-------------|
| `run_ids` (positional) | | One or more run IDs (or unique suffixes) |
| `--system-type` | required | System type: `database`, `message_queue`, `http_server` |
| `--plot-mode` | `score` | `score`, `combined`, or `metrics` |
| `--metrics` | `tokens,commits,tools,loc` | Comma-separated metrics for combined/metrics modes. Options: `tokens,commits,tools,loc,cost,steps` |
| `--max-hours` | | Drop score/metrics points whose elapsed time is greater than this many hours |
| `--score-source` | `output` | `output` (authoritative meta.json) or `workspace` (last_brief) |
| `--output` | `./score_trend_<type>_<run_id>.png` | Output PNG path; multi-run plots default to `*_multi.png` |
| `--title` | auto | Custom chart title |
| `--test-interval` | `900` | Fallback interval (sec) for synthetic X-axis when timestamps unavailable |
| `--workspace-root` | `workspace` | Workspace root directory |
| `--output-root` | `output` | Benchmark output root directory |
| `--logs-root` | `logs/runs` | Iteration logs root directory |
| `--output-json` | | Export meta JSON (auto-name or specify path) |
| `--input-json` | | Load meta JSON files instead of live data |
| `--show` | off | Show interactive chart window |

## X-axis Time

- Score curves use real `snapshot_time` from benchmark meta.json when all points have timestamps.
- Metrics curves are anchored to the run start time parsed from `run_id` when available.
- Combined plots force the visible origin to `(0, 0)` so score and metrics share the same T=0.
- `--max-hours` trims both score and metrics series before plotting/exporting.
- Falls back to synthetic time (`test_index * interval`) when timestamps are missing.

## Metric Semantics

- `tokens`, `commits`, `tools`, `cost`, and `steps` are cumulative per-iteration metrics derived from agent logs.
- `loc` means cumulative code lines changed, not lines added.
- `loc` is computed as `added + deleted` from snapshot-to-snapshot `git diff --numstat`.
- `loc` only counts source-like files and excludes generated or non-implementation paths such as `last_brief/`, `data/`, `wal/`, caches, and `spec/`.
- For fresh runs that have `logs/runs/<run_id>/baseline_snapshot.json`, iteration 0 is diffed against that run-start baseline so initialization-phase code changes are not lost when iteration 0 ends with multiple commits.
- `baseline_snapshot.json` is metrics-only bookkeeping: it does not create an extra plotted point and does not affect the run start time or test-runner triggering.
- Historical runs without a baseline snapshot still fall back to the previous snapshot, the snapshot commit parent, or the git empty tree.

## Meta JSON Schema

- **v1**: score points only (backward compatible with older exports).
- **v2**: score points + `metrics` array per series (written when metrics data is available).

Reading v2 JSON returns `EnrichedRunSeries` with `metrics_points`; v1 returns plain `RunSeries`.

## Notes

- Different `codeagent_model` values are shown in different colors.
- Combined mode requires exactly one run_id.
- Metrics mode requires iteration logs (`logs/runs/<run_id>/`) for metrics data; runs without logs show score only.
- Requires `matplotlib`:

```bash
pip install matplotlib
```
