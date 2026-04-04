"""Cline JSONL stdout parser."""

from __future__ import annotations

import json
import re
from collections import Counter, deque
from typing import Any

from metrics.models import IterationMetrics
from metrics.parsers.base import BaseAgentParser

_GIT_COMMIT_RE = re.compile(r"\bgit\s+commit\b")
_MEANINGFUL_SAY_TYPES = {"tool", "command", "completion_result"}
_READ_TOOL_NAMES = {"readFile"}
_WRITE_TOOL_NAMES = {"editedExistingFile", "newFileCreated"}
_TEST_COMMAND_RE = re.compile(
    r"\bpytest\b|\bpython(?:3)?\s+test[^/\s]*\.py\b|\bpython(?:3)?\s+-m\s+unittest\b|"
    r"\bfor\s+test\s+in\s+test_\*\.py\b",
    re.IGNORECASE,
)
_CONTEXT_WINDOW_RE = re.compile(
    r"Context Window Usage\s+([0-9,]+)\s*/\s*[0-9A-Za-z]+\s+tokens used",
    re.IGNORECASE,
)
_EXECUTE_COMMAND_RE = re.compile(r"\[execute_command for '(.+?)'\] Result:\n", re.DOTALL)
_EXIT_CODE_RE = re.compile(r"exit code (-?\d+)")
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


class ClineParser(BaseAgentParser):
    """Parse Cline's JSONL stdout into IterationMetrics.

    Cline's structured logs expose tool/file operations and shell commands, but
    do not currently emit reliable token or cost totals in iteration stdout.
    Those metrics are therefore reported as zero/None.
    """

    def supports_agent(self, agent_name: str) -> bool:
        return agent_name.lower() == "cline"

    def parse_iteration(self, iter_data: dict) -> IterationMetrics:
        iteration = iter_data["iteration"]
        agent = iter_data.get("agent", "cline")
        model = iter_data.get("model", "unknown")
        output = iter_data.get("output", {})
        success = output.get("success", False)
        duration = output.get("duration_seconds", 0.0)
        stdout = output.get("stdout", "")

        step_count = 0
        fallback_steps = 0
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
        max_context_window_used_tokens: int | None = None
        pending_commands: deque[str] = deque()

        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            ev_type = ev.get("type")
            text = ev.get("text")
            normalized_text = self._normalize_nested_text(text)
            if normalized_text:
                max_context_window_used_tokens = self._merge_context_usage(
                    max_context_window_used_tokens,
                    normalized_text,
                )

            if ev_type != "say":
                continue

            say_type = ev.get("say", "")
            if say_type == "api_req_started":
                step_count += 1
                exec_result = self._extract_execute_command_result(normalized_text or text)
                if exec_result is not None:
                    command_text = pending_commands.popleft() if pending_commands else exec_result["command"]
                    if exec_result["timed_out"]:
                        command_timeout_count += 1
                    elif exec_result["success"]:
                        command_success_count += 1
                    elif exec_result["failure"]:
                        command_failure_count += 1

                    if self._looks_like_test_command(command_text):
                        collected, passed = self._parse_test_metrics(exec_result["output"])
                        tests_collected += collected
                        tests_passed += passed
                continue

            if say_type == "tool":
                payload = self._parse_embedded_json(ev.get("text"))
                tool_name = payload.get("tool") if isinstance(payload.get("tool"), str) else "unknown"
                tool_counts[tool_name] += 1
                fallback_steps += 1
                if tool_name in _READ_TOOL_NAMES:
                    files_read_count += 1
                elif tool_name in _WRITE_TOOL_NAMES:
                    files_written_count += 1
                continue

            if say_type == "command":
                cmd = ev.get("text", "")
                command_count += 1
                if isinstance(cmd, str):
                    pending_commands.append(cmd)
                tool_counts["command"] += 1
                fallback_steps += 1
                if isinstance(cmd, str) and _GIT_COMMIT_RE.search(cmd):
                    commit_count += 1
                continue

            if say_type in _MEANINGFUL_SAY_TYPES:
                fallback_steps += 1

        if step_count == 0:
            step_count = fallback_steps

        total_tool_calls = sum(tool_counts.values())

        return IterationMetrics(
            iteration=iteration,
            agent=agent,
            model=model,
            duration_seconds=duration,
            success=success,
            tokens_input=0,
            tokens_output=0,
            tokens_reasoning=0,
            tokens_cache_read=0,
            tokens_cache_write=0,
            tokens_total=0,
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
            max_context_window_used_tokens=max_context_window_used_tokens,
            cost_usd=None,
        )

    @staticmethod
    def _parse_embedded_json(raw: Any) -> dict[str, Any]:
        if not isinstance(raw, str) or not raw.strip():
            return {}
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return {}
        return payload if isinstance(payload, dict) else {}

    @staticmethod
    def _normalize_nested_text(raw: Any) -> str:
        if not isinstance(raw, str) or not raw.strip():
            return ""
        stripped = raw.strip()
        if not stripped.startswith("{"):
            return raw
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return raw
        if not isinstance(payload, dict):
            return raw
        for key in ("request", "text", "content"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        return raw

    @staticmethod
    def _merge_context_usage(current: int | None, raw: str) -> int | None:
        matches = _CONTEXT_WINDOW_RE.findall(raw)
        if not matches:
            return current

        seen = current
        for used in matches:
            try:
                value = int(used.replace(",", ""))
            except ValueError:
                continue
            if seen is None:
                seen = value
            else:
                seen = max(seen, value)
        return seen

    @staticmethod
    def _looks_like_test_command(command: str | None) -> bool:
        return bool(command and _TEST_COMMAND_RE.search(command))

    @staticmethod
    def _extract_execute_command_result(raw: Any) -> dict[str, Any] | None:
        raw_text = ClineParser._normalize_nested_text(raw)
        if "[execute_command for '" not in raw_text:
            return None

        match = _EXECUTE_COMMAND_RE.search(raw_text)
        command = match.group(1) if match else None

        if match:
            body = raw_text[match.end():]
        else:
            body = raw_text

        env_marker = "\n<environment_details>"
        if env_marker in body:
            body = body.split(env_marker, 1)[0]

        body = body.strip()
        first_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
        timed_out = "Command timed out after" in first_line

        exit_code: int | None = None
        exit_match = _EXIT_CODE_RE.search(first_line)
        if exit_match:
            try:
                exit_code = int(exit_match.group(1))
            except ValueError:
                exit_code = None

        success = False
        failure = False
        if timed_out:
            failure = False
        elif exit_code is not None:
            success = exit_code == 0
            failure = exit_code != 0
        elif "Command executed successfully" in first_line:
            success = True
        elif "Command failed" in first_line:
            failure = True

        output_text = ""
        for marker in ("Output so far:\n", "Output:\n"):
            if marker in body:
                output_text = body.split(marker, 1)[1].strip()
                break

        return {
            "command": command,
            "success": success,
            "failure": failure,
            "timed_out": timed_out,
            "output": output_text,
        }

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
