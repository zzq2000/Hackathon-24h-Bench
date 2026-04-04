"""Plot score trends from workspace last_brief test summaries."""

from .cli import main
from .core import (
    EnrichedRunSeries,
    MetricsPoint,
    compute_elapsed_hours,
    load_enriched_run_series,
    load_many_enriched_series,
    load_run_series_from_output,
    load_many_series_from_output,
)

__all__ = [
    "main",
    "MetricsPoint",
    "EnrichedRunSeries",
    "compute_elapsed_hours",
    "load_enriched_run_series",
    "load_many_enriched_series",
    "load_run_series_from_output",
    "load_many_series_from_output",
]

