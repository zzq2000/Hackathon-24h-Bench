"""Codex JSONL stdout parser."""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

from metrics.models import IterationMetrics
from metrics.parsers.base import BaseAgentParser

_GIT_COMMIT_RE = re.compile(r"\bgit\s+commit\b")
_TEST_COMMAND_RE = re.compile(
    r"\bpytest\b|\bpython(?:3)?\s+test[^/\s]*\.py\b|\bpython(?:3)?\s+-m\s+unittest\b|"
    r"\bfor\s+test\s+in\s+test_\*\.py\b",
    re.IGNORECASE,
)
_COLLECTED_RE = re.compile(r"\bcollected\s+(\d+)\s+items?\b", re.IGNORECASE)
_PYTEST_PASSED_RE = re.compile(r"\b(\d+)\s+passed(?:,\s*\d+\s+warnings?)?\s+in\b", re.IGNORECASE)
_RESULTS_PASSED_FAILED_RE = re.compile(
    r"\bResults?:\s*(\d+)\s+passed,\s*(\d+)\s+failed(?:,\s*(\d+)\s+errors?)?\b",
    re.IGNORECASE,
)
_INLINE_PASSED_FAILED_RE = re.compile(
    r"\b(\d+)\s+passed,\s*(\d+)\s+failed(?:,\s*(\d+)\s+errors?)?\b",
    re.IGNORECASE,
)
_RESULTS_TOTAL_RE = re.compile(
    r"\bResults?:\s*(\d+)\s+tests?,\s*(\d+)\s+failures?,\s*(\d+)\s+errors?\b",
    re.IGNORECASE,
)
_FRACTION_PASSED_RE = re.compile(r"\b(\d+)\s*/\s*(\d+)\s+tests?\s+passed\b", re.IGNORECASE)
_RAN_TESTS_RE = re.compile(r"\bRan\s+(\d+)\s+tests?\b")
_FAILED_DETAILS_RE = re.compile(r"(failures?|errors?)=(\d+)", re.IGNORECASE)
_TOOL_ITEM_TYPES = {"command_execution", "file_change", "mcp_tool_call", "web_search", "todo_list"}


class CodexParser(BaseAgentParser):
    """Parse Codex CLI JSONL stdout into IterationMetrics."""

    def supports_agent(self, agent_name: str) -> bool:
        return agent_name.lower() == "codex"

    def parse_iteration(self, iter_data: dict) -> IterationMetrics:
        iteration = iter_data["iteration"]
        agent = iter_data.get("agent", "codex")
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
        step_count = 0
        turn_count = 0
        tool_counts: Counter[str] = Counter()
        commit_count = 0
        command_count = 0
        command_success_count = 0
        command_failure_count = 0
        command_timeout_count = 0
        files_read_count = 0
        files_written_count = 0
        tests_collected = 0
        tests_passed = 0
        seen_steps: set[str] = set()

        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if not isinstance(ev, dict):
                continue

            ev_type = ev.get("type")

            if ev_type == "turn.completed":
                usage = self._extract_usage(ev)
                tokens_input += usage.get("input_tokens", 0)
                tokens_output += usage.get("output_tokens", 0)
                tokens_reasoning += usage.get("reasoning_tokens", 0)
                tokens_cache_read += usage.get("cached_input_tokens", 0)
                turn_count += 1
                continue

            if ev_type != "item.completed":
                continue

            item = ev.get("item", {})
            if not isinstance(item, dict):
                continue

            item_id = item.get("id")
            if isinstance(item_id, str):
                seen_steps.add(item_id)
            else:
                step_count += 1

            item_type = item.get("type", "unknown")

            if item_type == "command_execution":
                tool_counts["command_execution"] += 1
                command_count += 1
                command_text = self._extract_command_text(item)
                if command_text and _GIT_COMMIT_RE.search(command_text):
                    commit_count += 1

                command_output = self._extract_command_output(item)
                result_state = self._classify_command_result(item, command_output)
                if result_state == "timeout":
                    command_timeout_count += 1
                elif result_state == "success":
                    command_success_count += 1
                elif result_state == "failure":
                    command_failure_count += 1

                if self._looks_like_test_command(command_text):
                    collected, passed = self._parse_test_metrics(command_output)
                    tests_collected += collected
                    tests_passed += passed
                continue

            if item_type == "file_change":
                tool_counts["file_change"] += 1
                files_written_count += self._count_file_changes(item)
                continue

            if item_type == "mcp_tool_call":
                tool_counts[self._mcp_tool_label(item)] += 1
                continue

            if item_type in _TOOL_ITEM_TYPES:
                tool_counts[item_type] += 1

        if seen_steps:
            step_count += len(seen_steps)
        if step_count == 0:
            step_count = turn_count

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
            tokens_reasoning=tokens_reasoning,
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
            command_timeout_count=command_timeout_count,
            files_read_count=files_read_count,
            files_written_count=files_written_count,
            tests_collected=tests_collected,
            tests_passed=tests_passed,
            cost_usd=None,
        )

    @staticmethod
    def _extract_usage(ev: dict[str, Any]) -> dict[str, int]:
        raw = ev.get("usage")
        if not isinstance(raw, dict):
            raw = ev.get("response", {}).get("usage", {}) if isinstance(ev.get("response"), dict) else {}
        if not isinstance(raw, dict):
            raw = {}
        return {
            "input_tokens": int(raw.get("input_tokens", 0) or 0),
            "output_tokens": int(raw.get("output_tokens", 0) or 0),
            "cached_input_tokens": int(raw.get("cached_input_tokens", 0) or 0),
            "reasoning_tokens": int(
                raw.get("reasoning_output_tokens", raw.get("reasoning_tokens", 0)) or 0
            ),
        }

    @staticmethod
    def _extract_command_text(item: dict[str, Any]) -> str:
        for key in ("command", "input", "text"):
            value = item.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                command = value.get("command")
                if isinstance(command, str):
                    return command
        return ""

    @staticmethod
    def _extract_command_output(item: dict[str, Any]) -> str:
        for key in ("aggregated_output", "output", "text", "stderr", "stdout"):
            value = item.get(key)
            if isinstance(value, str):
                return value
        return ""

    @staticmethod
    def _classify_command_result(item: dict[str, Any], output: str) -> str:
        if CodexParser._is_timeout(item, output):
            return "timeout"

        exit_code = item.get("exit_code")
        if isinstance(exit_code, int):
            return "success" if exit_code == 0 else "failure"
        status = str(item.get("status", "")).lower()
        if status in {"completed", "success", "succeeded"}:
            return "success"
        if status in {"failed", "error"}:
            return "failure"
        error = item.get("error")
        if isinstance(error, str) and error.strip():
            return "failure"
        return "unknown"

    @staticmethod
    def _is_timeout(item: dict[str, Any], output: str) -> bool:
        status = str(item.get("status", "")).lower()
        if "timeout" in status:
            return True
        error = item.get("error")
        if isinstance(error, str) and "timeout" in error.lower():
            return True
        return "timed out" in output.lower()

    @staticmethod
    def _count_file_changes(item: dict[str, Any]) -> int:
        changes = item.get("changes")
        if not isinstance(changes, list):
            return 1

        seen_paths: set[str] = set()
        for change in changes:
            if not isinstance(change, dict):
                continue
            path = change.get("path")
            if isinstance(path, str) and path:
                seen_paths.add(path)
        return len(seen_paths) if seen_paths else max(1, len(changes))

    @staticmethod
    def _mcp_tool_label(item: dict[str, Any]) -> str:
        server = item.get("server")
        tool = item.get("tool")
        if isinstance(server, str) and isinstance(tool, str):
            return f"mcp:{server}/{tool}"
        return "mcp_tool_call"

    @staticmethod
    def _looks_like_test_command(command: str) -> bool:
        return bool(command and _TEST_COMMAND_RE.search(command))

    @staticmethod
    def _parse_test_metrics(output_text: str) -> tuple[int, int]:
        if not output_text.strip():
            return 0, 0

        collected = 0
        passed = 0
        pending_ran: int | None = None

        for raw_line in output_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            fraction_match = _FRACTION_PASSED_RE.search(line)
            if fraction_match:
                passed += int(fraction_match.group(1))
                collected += int(fraction_match.group(2))
                pending_ran = None
                continue

            results_match = _RESULTS_PASSED_FAILED_RE.search(line)
            if results_match:
                pass_count = int(results_match.group(1))
                fail_count = int(results_match.group(2))
                err_count = int(results_match.group(3) or 0)
                passed += pass_count
                collected += pass_count + fail_count + err_count
                pending_ran = None
                continue

            total_match = _RESULTS_TOTAL_RE.search(line)
            if total_match:
                total = int(total_match.group(1))
                fail_count = int(total_match.group(2))
                err_count = int(total_match.group(3))
                collected += total
                passed += max(0, total - fail_count - err_count)
                pending_ran = None
                continue

            collected_match = _COLLECTED_RE.search(line)
            if collected_match:
                collected += int(collected_match.group(1))
                pending_ran = None
                continue

            pytest_match = _PYTEST_PASSED_RE.search(line)
            if pytest_match:
                passed += int(pytest_match.group(1))
                pending_ran = None
                continue

            inline_match = _INLINE_PASSED_FAILED_RE.search(line)
            if inline_match:
                pass_count = int(inline_match.group(1))
                fail_count = int(inline_match.group(2))
                err_count = int(inline_match.group(3) or 0)
                passed += pass_count
                collected += pass_count + fail_count + err_count
                pending_ran = None
                continue

            ran_match = _RAN_TESTS_RE.search(line)
            if ran_match:
                pending_ran = int(ran_match.group(1))
                continue

            if pending_ran is not None and line.upper() == "OK":
                collected += pending_ran
                passed += pending_ran
                pending_ran = None
                continue

            if pending_ran is not None and line.upper().startswith("FAILED"):
                failures = 0
                for key, value in _FAILED_DETAILS_RE.findall(line):
                    if key.lower().startswith(("failure", "error")):
                        failures += int(value)
                collected += pending_ran
                passed += max(0, pending_ran - failures)
                pending_ran = None

        return collected, passed
