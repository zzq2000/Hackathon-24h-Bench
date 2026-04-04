"""Claude Code JSONL stdout parser."""

from __future__ import annotations

import json
import re
from collections import Counter

from metrics.models import IterationMetrics
from metrics.parsers.base import BaseAgentParser

# Pattern to detect git commit commands in bash tool calls
_GIT_COMMIT_RE = re.compile(r"\bgit\s+commit\b")


class ClaudeParser(BaseAgentParser):
    """Parse Claude Code's JSONL stdout into IterationMetrics."""

    def supports_agent(self, agent_name: str) -> bool:
        return agent_name.lower() == "claude"

    def parse_iteration(self, iter_data: dict) -> IterationMetrics:
        iteration = iter_data["iteration"]
        agent = iter_data.get("agent", "claude")
        model = iter_data.get("model", "unknown")
        output = iter_data.get("output", {})
        success = output.get("success", False)
        duration = output.get("duration_seconds", 0.0)
        stdout = output.get("stdout", "")

        tokens_input = 0
        tokens_output = 0
        tokens_cache_read = 0
        tokens_cache_write = 0
        step_count = 0
        cost_usd: float | None = None
        tool_counts: Counter[str] = Counter()
        commit_count = 0
        command_count = 0
        command_success_count = 0
        command_failure_count = 0
        files_read_count = 0
        files_written_count = 0

        # Track tool_use_id -> tool_name for matching with tool_result events
        tool_id_to_name: dict[str, str] = {}

        for line in stdout.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            ev_type = ev.get("type", "")

            if ev_type == "result":
                # Aggregated token usage from the result event
                usage = ev.get("usage", {})
                tokens_input += usage.get("input_tokens", 0)
                tokens_output += usage.get("output_tokens", 0)
                tokens_cache_read += usage.get("cache_read_input_tokens", 0)
                tokens_cache_write += usage.get("cache_creation_input_tokens", 0)
                step_count = ev.get("num_turns", 0)
                raw_cost = ev.get("total_cost_usd")
                if raw_cost is not None:
                    cost_usd = float(raw_cost)

            elif ev_type == "assistant":
                message = ev.get("message", {})
                content_blocks = message.get("content", [])
                for block in content_blocks:
                    if block.get("type") == "tool_use":
                        tool_name = block.get("name", "unknown")
                        tool_id = block.get("id", "")
                        tool_counts[tool_name] += 1
                        if tool_id:
                            tool_id_to_name[tool_id] = tool_name
                        if tool_name == "Bash":
                            command_count += 1
                            inp = block.get("input", {})
                            cmd = inp.get("command", "")
                            if _GIT_COMMIT_RE.search(cmd):
                                commit_count += 1
                        elif tool_name == "Read":
                            files_read_count += 1
                        elif tool_name in ("Write", "Edit"):
                            files_written_count += 1

            elif ev_type == "user":
                # tool_result blocks carry is_error for Bash success/failure
                for block in ev.get("message", {}).get("content", []):
                    if block.get("type") == "tool_result":
                        tid = block.get("tool_use_id", "")
                        name = tool_id_to_name.get(tid, "")
                        if name == "Bash":
                            if block.get("is_error", False):
                                command_failure_count += 1
                            else:
                                command_success_count += 1

        tokens_total = tokens_input + tokens_output
        total_tool_calls = sum(tool_counts.values())

        return IterationMetrics(
            iteration=iteration,
            agent=agent,
            model=model,
            duration_seconds=duration,
            success=success,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_reasoning=0,
            tokens_cache_read=tokens_cache_read,
            tokens_cache_write=tokens_cache_write,
            tokens_total=tokens_total,
            step_count=step_count,
            tool_calls=dict(tool_counts),
            total_tool_calls=total_tool_calls,
            commit_count=commit_count,
            command_count=command_count,
            command_success_count=command_success_count,
            command_failure_count=command_failure_count,
            files_read_count=files_read_count,
            files_written_count=files_written_count,
            cost_usd=cost_usd,
        )
