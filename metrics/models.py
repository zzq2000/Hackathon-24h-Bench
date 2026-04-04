"""Data models for metrics."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class IterationMetrics:
    iteration: int
    agent: str
    model: str
    duration_seconds: float
    success: bool
    # Token metrics (summed across all steps in iteration)
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_reasoning: int = 0
    tokens_cache_read: int = 0
    tokens_cache_write: int = 0
    tokens_total: int = 0
    # Steps
    step_count: int = 0
    # Tool usage: {"bash": 54, "read": 16, ...}
    tool_calls: dict[str, int] = field(default_factory=dict)
    total_tool_calls: int = 0
    # Commits detected (from bash git commit commands)
    commit_count: int = 0
    # Shell command activity (best-effort for agents that expose command logs)
    command_count: int = 0
    command_success_count: int = 0
    command_failure_count: int = 0
    command_timeout_count: int = 0
    # File operations (best-effort for agents that expose tool/file events)
    files_read_count: int = 0
    files_written_count: int = 0
    # Observed test execution summaries
    tests_collected: int = 0
    tests_passed: int = 0
    # Maximum context window usage reported during the iteration
    max_context_window_used_tokens: int | None = None
    # Cost in USD (when reported by the agent, e.g. Claude)
    cost_usd: float | None = None
    # Workspace code lines changed in this iteration (added + deleted, source files only)
    workspace_loc_added: int | None = None
    # Warning message when workspace code delta could not be computed.
    workspace_loc_issue: str | None = None
    # Snapshot commit SHA and timestamp (from snapshots/)
    snapshot_commit: str | None = None
    snapshot_timestamp: str | None = None
    # Iteration log timestamp (from iterations/ 'timestamp' field)
    iteration_timestamp: str | None = None


@dataclass
class BenchmarkSnapshot:
    test_index: int
    score: float
    overall_status: str
    passed_count: int
    total_count: int
    test_start: str
    test_end: str
    error: str | None = None
    snapshot_time: str | None = None
    # Linked iteration index (set by benchmark_linker)
    linked_iteration: int | None = None


@dataclass
class RunMetrics:
    run_id: str
    agent: str
    model: str
    iterations: list[IterationMetrics] = field(default_factory=list)
    benchmarks: list[BenchmarkSnapshot] = field(default_factory=list)
    # Aggregated totals
    total_tokens: int = 0
    total_tool_calls: int = 0
    total_commits: int = 0
    total_commands: int = 0
    total_command_successes: int = 0
    total_command_failures: int = 0
    total_command_timeouts: int = 0
    total_files_read: int = 0
    total_files_written: int = 0
    total_tests_collected: int = 0
    total_tests_passed: int = 0
    peak_context_window_used_tokens: int | None = None
    total_workspace_loc_added: int | None = None
    total_duration_seconds: float = 0.0
    tool_call_summary: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
