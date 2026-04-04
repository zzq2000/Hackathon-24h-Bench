"""Gemini CLI JSON parser."""

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
_STREAM_EVENT_TYPES = {"init", "message", "tool_use", "tool_result", "error", "result"}
_COMMAND_TOOL_HINTS = ("shell", "bash", "command", "exec", "run")
_READ_TOOL_HINTS = ("read", "cat", "glob", "grep", "search", "find", "ls")
_WRITE_TOOL_HINTS = ("write", "edit", "replace", "patch", "create", "mkdir", "delete")


class GeminiParser(BaseAgentParser):
    """Parse Gemini CLI JSON/stdout formats into IterationMetrics."""

    def supports_agent(self, agent_name: str) -> bool:
        return agent_name.lower() == "gemini"

    def parse_iteration(self, iter_data: dict) -> IterationMetrics:
        iteration = iter_data["iteration"]
        agent = iter_data.get("agent", "gemini")
        model = iter_data.get("model", "unknown")
        output = iter_data.get("output", {})
        success = output.get("success", False)
        duration = output.get("duration_seconds", 0.0)
        stdout = output.get("stdout", "")

        stream_events = self._parse_stream_events(stdout)
        if stream_events:
            return self._parse_stream_iteration(
                iteration=iteration,
                agent=agent,
                model=model,
                duration=duration,
                success=success,
                events=stream_events,
            )

        return self._parse_summary_iteration(
            iteration=iteration,
            agent=agent,
            model=model,
            duration=duration,
            success=success,
            stdout=stdout,
        )

    def _parse_stream_iteration(
        self,
        *,
        iteration: int,
        agent: str,
        model: str,
        duration: float,
        success: bool,
        events: list[dict[str, Any]],
    ) -> IterationMetrics:
        tokens_input = 0
        tokens_output = 0
        tokens_cache_read = 0
        tokens_total = 0
        step_count = 0
        assistant_turns = 0
        assistant_open = False
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
        pending_tools: dict[str, dict[str, Any]] = {}

        for ev in events:
            ev_type = ev.get("type")

            if ev_type == "message":
                if ev.get("role") == "assistant":
                    if not assistant_open:
                        assistant_turns += 1
                        assistant_open = True
                else:
                    assistant_open = False
                continue

            assistant_open = False

            if ev_type == "tool_use":
                tool_name = self._tool_name(ev.get("tool_name"))
                tool_id = str(ev.get("tool_id") or f"tool-{command_count}-{len(pending_tools)}")
                params = ev.get("parameters", {})
                if not isinstance(params, dict):
                    params = {}
                pending_tools[tool_id] = {"name": tool_name, "parameters": params}
                tool_counts[tool_name] += 1
                step_count += 1

                if self._is_read_tool(tool_name, params):
                    files_read_count += 1
                if self._is_write_tool(tool_name, params):
                    files_written_count += 1
                if self._is_command_tool(tool_name, params):
                    command_count += 1
                    command_text = self._extract_command_text(params)
                    if command_text and _GIT_COMMIT_RE.search(command_text):
                        commit_count += 1
                continue

            if ev_type == "tool_result":
                tool_id = str(ev.get("tool_id") or "")
                pending = pending_tools.get(tool_id, {})
                tool_name = self._tool_name(pending.get("name"))
                params = pending.get("parameters", {})
                if not isinstance(params, dict):
                    params = {}
                if self._is_command_tool(tool_name, params):
                    output_text = ev.get("output", "")
                    if not isinstance(output_text, str):
                        output_text = ""
                    error_info = ev.get("error", {})
                    if not isinstance(error_info, dict):
                        error_info = {}

                    if self._is_timeout(ev, error_info, output_text):
                        command_timeout_count += 1
                    elif ev.get("status") == "success":
                        command_success_count += 1
                    else:
                        command_failure_count += 1

                    command_text = self._extract_command_text(params)
                    if self._looks_like_test_command(command_text):
                        collected, passed = self._parse_test_metrics(
                            output_text or str(error_info.get("message", ""))
                        )
                        tests_collected += collected
                        tests_passed += passed
                continue

            if ev_type == "result":
                stats = ev.get("stats", {})
                if isinstance(stats, dict):
                    tokens_input += int(stats.get("input_tokens", 0) or 0)
                    tokens_output += int(stats.get("output_tokens", 0) or 0)
                    tokens_cache_read += int(stats.get("cached", 0) or 0)
                    tokens_total += int(stats.get("total_tokens", 0) or 0)

        total_tool_calls = sum(tool_counts.values())
        if step_count == 0:
            step_count = assistant_turns or (1 if events else 0)
        else:
            step_count += assistant_turns
        if tokens_total == 0:
            tokens_total = tokens_input + tokens_output

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
            tokens_cache_write=0,
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

    def _parse_summary_iteration(
        self,
        *,
        iteration: int,
        agent: str,
        model: str,
        duration: float,
        success: bool,
        stdout: str,
    ) -> IterationMetrics:
        try:
            payload = json.loads(stdout)
        except (json.JSONDecodeError, ValueError):
            payload = {}

        if not isinstance(payload, dict):
            payload = {}

        stats = payload.get("stats", {})
        if not isinstance(stats, dict):
            stats = {}

        tokens_input = 0
        tokens_output = 0
        tokens_reasoning = 0
        tokens_cache_read = 0
        tokens_total = 0
        step_count = 0
        tool_counts: Counter[str] = Counter()
        command_count = 0
        command_success_count = 0
        command_failure_count = 0
        files_read_count = 0
        files_written_count = 0

        models = stats.get("models", {})
        if isinstance(models, dict):
            for model_metrics in models.values():
                if not isinstance(model_metrics, dict):
                    continue
                api = model_metrics.get("api", {})
                tokens = model_metrics.get("tokens", {})
                if isinstance(api, dict):
                    step_count += int(api.get("totalRequests", 0) or 0)
                if not isinstance(tokens, dict):
                    continue
                tokens_input += int(tokens.get("prompt", 0) or 0)
                tokens_output += int(tokens.get("candidates", 0) or 0)
                tokens_reasoning += int(tokens.get("thoughts", 0) or 0)
                tokens_cache_read += int(tokens.get("cached", 0) or 0)
                tokens_total += int(tokens.get("total", 0) or 0)

        tools = stats.get("tools", {})
        if isinstance(tools, dict):
            by_name = tools.get("byName", {})
            if isinstance(by_name, dict):
                for raw_name, raw_metrics in by_name.items():
                    tool_name = self._tool_name(raw_name)
                    if not isinstance(raw_metrics, dict):
                        continue
                    count = int(raw_metrics.get("count", 0) or 0)
                    tool_counts[tool_name] += count
                    if self._is_command_tool(tool_name, {}):
                        command_count += count
                        command_success_count += int(raw_metrics.get("success", 0) or 0)
                        command_failure_count += int(raw_metrics.get("fail", 0) or 0)
                    if self._is_read_tool(tool_name, {}):
                        files_read_count += count
                    if self._is_write_tool(tool_name, {}):
                        files_written_count += count

        total_tool_calls = int(tools.get("totalCalls", 0) or 0) if isinstance(tools, dict) else 0
        if total_tool_calls == 0:
            total_tool_calls = sum(tool_counts.values())
        if tokens_total == 0:
            tokens_total = tokens_input + tokens_output + tokens_reasoning
        if step_count == 0:
            step_count = total_tool_calls

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
            tokens_cache_write=0,
            tokens_total=tokens_total,
            step_count=step_count,
            tool_calls=dict(tool_counts),
            total_tool_calls=total_tool_calls,
            commit_count=0,
            command_count=command_count,
            command_success_count=command_success_count,
            command_failure_count=command_failure_count,
            command_timeout_count=0,
            files_read_count=files_read_count,
            files_written_count=files_written_count,
            tests_collected=0,
            tests_passed=0,
            cost_usd=None,
        )

    @staticmethod
    def _parse_stream_events(stdout: str) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if isinstance(payload, dict) and payload.get("type") in _STREAM_EVENT_TYPES:
                events.append(payload)
        return events

    @staticmethod
    def _tool_name(raw_name: Any) -> str:
        return raw_name if isinstance(raw_name, str) and raw_name else "unknown"

    @staticmethod
    def _extract_command_text(parameters: dict[str, Any]) -> str:
        for key in ("command", "cmd", "shell_command"):
            value = parameters.get(key)
            if isinstance(value, str):
                return value
        return ""

    @staticmethod
    def _is_command_tool(tool_name: str, parameters: dict[str, Any]) -> bool:
        lowered = tool_name.lower()
        if any(hint in lowered for hint in _COMMAND_TOOL_HINTS):
            return True
        return isinstance(parameters.get("command"), str) or isinstance(parameters.get("cmd"), str)

    @staticmethod
    def _is_read_tool(tool_name: str, parameters: dict[str, Any]) -> bool:
        if GeminiParser._is_write_tool(tool_name, parameters):
            return False
        lowered = tool_name.lower()
        if any(hint in lowered for hint in _READ_TOOL_HINTS):
            return True
        return any(isinstance(parameters.get(key), str) for key in ("pattern", "glob"))

    @staticmethod
    def _is_write_tool(tool_name: str, parameters: dict[str, Any]) -> bool:
        lowered = tool_name.lower()
        if any(hint in lowered for hint in _WRITE_TOOL_HINTS):
            return True
        return any(isinstance(parameters.get(key), str) for key in ("old_string", "new_string", "content"))

    @staticmethod
    def _is_timeout(event: dict[str, Any], error_info: dict[str, Any], output_text: str) -> bool:
        if str(event.get("status", "")).lower() == "timeout":
            return True
        message = str(error_info.get("message", ""))
        if "timeout" in message.lower():
            return True
        return "timed out" in output_text.lower()

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
