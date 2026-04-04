"""OpenCode JSONL stdout parser."""

from __future__ import annotations

import json
import re
from collections import Counter

from metrics.models import IterationMetrics
from metrics.parsers.base import BaseAgentParser

# Pattern to detect git commit commands in bash tool calls
_GIT_COMMIT_RE = re.compile(r"\bgit\s+commit\b")


class OpenCodeParser(BaseAgentParser):
    """Parse OpenCode's JSONL stdout into IterationMetrics."""

    def supports_agent(self, agent_name: str) -> bool:
        return agent_name.lower() == "opencode"

    def parse_iteration(self, iter_data: dict) -> IterationMetrics:
        iteration = iter_data["iteration"]
        agent = iter_data.get("agent", "opencode")
        model = iter_data.get("model", "unknown")
        output = iter_data.get("output", {})
        success = output.get("success", False)
        duration = output.get("duration_seconds", 0.0)
        stdout = output.get("stdout", "")

        tokens_input = 0
        tokens_output = 0
        tokens_reasoning = 0
        tokens_cache_read = 0
        tokens_cache_write = 0
        tokens_total = 0
        step_count = 0
        tool_counts: Counter[str] = Counter()
        commit_count = 0

        for line in stdout.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            ev_type = ev.get("type", "")
            part = ev.get("part", {})

            if ev_type == "step_start":
                step_count += 1

            elif ev_type == "step_finish":
                tokens = part.get("tokens", {})
                tokens_input += tokens.get("input", 0)
                tokens_output += tokens.get("output", 0)
                tokens_reasoning += tokens.get("reasoning", 0)
                tokens_total += tokens.get("total", 0)
                cache = tokens.get("cache", {})
                tokens_cache_read += cache.get("read", 0)
                tokens_cache_write += cache.get("write", 0)

            elif ev_type == "tool_use":
                tool_name = part.get("tool", "unknown")
                tool_counts[tool_name] += 1
                # Detect git commit commands in bash tool calls
                if tool_name == "bash":
                    state = part.get("state", {})
                    inp = state.get("input", {})
                    cmd = inp.get("command", "")
                    if _GIT_COMMIT_RE.search(cmd):
                        commit_count += 1

        total_tool_calls = sum(tool_counts.values())

        return IterationMetrics(
            iteration=iteration,
            agent=agent,
            model=model,
            duration_seconds=duration,
            success=success,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            tokens_reasoning=tokens_reasoning,
            tokens_cache_read=tokens_cache_read,
            tokens_cache_write=tokens_cache_write,
            tokens_total=tokens_total,
            step_count=step_count,
            tool_calls=dict(tool_counts),
            total_tool_calls=total_tool_calls,
            commit_count=commit_count,
        )
