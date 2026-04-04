"""
HTTP Server Benchmark Runner Implementation.

Runs HTTP/1.1 benchmark suites against web server implementations.

Three benchmark suites, mapped to progressive tiers (L0-L4):
  - h1spec:  HTTP/1.1 protocol conformance testing
  - cispa:   cispa/http-conformance HTTP/1.1 conformance rules
  - tfb:     TechEmpower Framework Benchmarks correctness verification

Tier mapping:
  L0 -> h1spec (~33 tests)
  L1 -> cispa (curated HTTP/1.1 subset)
  L2 -> tfb (plaintext + json)
  L3 -> tfb (db + query)
  L4 -> tfb (fortune + update)
"""

from __future__ import annotations

import ast
import json
import logging
import math
import os
import re
import socket
import shutil
import subprocess
import sys
import time
import importlib.util
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import tomllib
except Exception:  # pragma: no cover - fallback for older Python runtimes
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except Exception:
        tomllib = None

from ..base import BenchmarkResult, BenchmarkRunner, BenchmarkStatus

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# TFB test types
# ---------------------------------------------------------------------------
TFB_TEST_TYPES: List[str] = [
    "plaintext", "json", "db", "query", "fortune", "update",
]

SUPPORTED_SUITES: Tuple[str, ...] = ("cispa", "tfb", "h1spec")
CISPA_CURATED_CORE_RULES: Tuple[str, ...] = (
    "content_head_request",
    "reject_msgs_with_whitespace_between_startline_and_first_header_field",
    "code_400_if_msg_with_whitespace_between_header_field_and_colon",
    "duplicate_fields",
    "transfer_encoding_http11",
    "post_invalid_response_codes",
    "no_bare_cr",
    "content_length_same_head_get",
)
CISPA_CORE_POINTS = len(CISPA_CURATED_CORE_RULES)
CISPA_FULL_POINTS = 106
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_RULESET_DIR = PROJECT_ROOT / "benchmarks" / "rulesets"


@dataclass
class HttpBenchConfig:
    """Configuration for the HTTP benchmark runner."""

    network_mode: str = "host"
    cispa_repo: str = "https://github.com/cispa/http-conformance.git"
    cispa_timeout_sec: int = 120
    cispa_mode: str = "core_subset"  # "core_subset" or "full"
    cispa_postgres_image: str = "postgres:15-alpine"
    cispa_postgres_startup_sec: int = 30
    tfb_repo: str = "https://github.com/TechEmpower/FrameworkBenchmarks.git"
    tfb_timeout_sec: int = 300
    tfb_tests: List[str] = field(default_factory=list)
    h1spec_repo: str = "https://github.com/uNetworking/h1spec"
    h1spec_deno_image: str = "denoland/deno:alpine-2.1.4"
    h1spec_script_url: str = "https://raw.githubusercontent.com/uNetworking/h1spec/master/http_test.ts"
    h1spec_timeout_sec: int = 120
    suites: List[str] = field(default_factory=list)


class HttpBenchRunner(BenchmarkRunner):
    """HTTP server benchmark runner (cispa / TFB / h1spec)."""

    name = "http_bench"
    description = "HTTP/1.1 benchmark (cispa conformance, TFB verification, h1spec)"
    supported_suts = ["http_server"]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._docker_probe: Optional[Tuple[bool, str]] = None
        self._cispa_repo_dir: Optional[Path] = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(
        self,
        sut_host: str,
        sut_port: int,
        output_dir: Path,
        timeout_sec: int = 600,
        **kwargs,
    ) -> BenchmarkResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        start_time = time.time()
        benchmark_deadline = start_time + max(0, timeout_sec)

        tier = str(kwargs.get("tier") or "").strip()
        bench_config = self._get_config(kwargs)

        suites = self._select_suites(bench_config, tier=tier)
        unknown_suites = sorted({s for s in suites if s not in SUPPORTED_SUITES})
        if unknown_suites:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error=(
                    f"Unsupported http_bench suite(s): {', '.join(unknown_suites)}. "
                    f"Supported suites: {', '.join(SUPPORTED_SUITES)}"
                ),
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )
        if not suites:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error="No enabled suites in http_bench config",
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )

        workload_results: Dict[str, str] = {}
        all_metrics: Dict[str, Any] = {}
        all_errors: List[str] = []
        all_runtime_errors: List[str] = []

        if "cispa" in suites:
            logger.info("Running http_bench suite: cispa")
            cispa_results, cispa_metrics = self._run_cispa_suite(
                sut_host, sut_port, bench_config, raw_dir, benchmark_deadline
            )
            workload_results.update(cispa_results)
            all_metrics["cispa"] = cispa_metrics
            cispa_failures = [
                k for k, v in cispa_results.items()
                if v not in {"PASS", "SKIP", "RUNTIME_ERROR"}
            ]
            if cispa_metrics.get("runtime_error"):
                runtime_msg = str(cispa_metrics.get("error") or "cispa runtime error")
                all_runtime_errors.append(runtime_msg)
            if cispa_failures:
                err_summary = f"cispa: {len(cispa_failures)} rule(s) failed"
                all_errors.append(err_summary)

        if "tfb" in suites:
            logger.info("Running http_bench suite: tfb")
            tfb_results, tfb_metrics = self._run_tfb_suite(
                sut_host, sut_port, bench_config, raw_dir, benchmark_deadline
            )
            workload_results.update(tfb_results)
            all_metrics["tfb"] = tfb_metrics
            tfb_failures = [k for k, v in tfb_results.items() if v != "PASS"]
            if tfb_failures:
                err_summary = f"tfb: {len(tfb_failures)} test(s) failed"
                first_err = self._first_workload_error(tfb_metrics, tfb_failures)
                if first_err:
                    err_summary += f" (first error: {first_err})"
                all_errors.append(err_summary)

        if "h1spec" in suites:
            logger.info("Running http_bench suite: h1spec")
            h1_results, h1_metrics = self._run_h1spec_suite(
                sut_host, sut_port, bench_config, raw_dir, benchmark_deadline
            )
            workload_results.update(h1_results)
            all_metrics["h1spec"] = h1_metrics
            h1_failures = [k for k, v in h1_results.items() if v != "PASS"]
            if h1_failures:
                err_summary = f"h1spec: {len(h1_failures)} workload(s) failed"
                first_err = self._first_workload_error(h1_metrics, h1_failures)
                if first_err:
                    err_summary += f" (first error: {first_err})"
                all_errors.append(err_summary)

        non_pass = {status for status in workload_results.values() if status not in {"PASS", "SKIP"}}
        if all_runtime_errors:
            status = BenchmarkStatus.RUNTIME_ERROR
        elif not non_pass:
            status = BenchmarkStatus.ACCEPTED
        elif non_pass <= {"TIMEOUT"}:
            status = BenchmarkStatus.TIME_LIMIT_EXCEEDED
        elif all_errors:
            status = BenchmarkStatus.WRONG_ANSWER
        else:
            status = BenchmarkStatus.WRONG_ANSWER
        score = self._calculate_score(workload_results)

        # Persist results
        (output_dir / "http_bench_results.json").write_text(
            json.dumps(
                {
                    "tier": tier,
                    "suites": suites,
                    "workload_results": workload_results,
                    "metrics": all_metrics,
                },
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        detail_parts: List[str] = []
        if all_runtime_errors:
            detail_parts.append(f"runtime: {'; '.join(all_runtime_errors)}")
        if all_errors:
            detail_parts.append(f"failures: {'; '.join(all_errors)}")
        details = "HTTP Bench: " + "; ".join(detail_parts) if detail_parts else "All suites passed"

        error_parts: List[str] = []
        if all_runtime_errors:
            error_parts.extend(all_runtime_errors)
        if all_errors:
            error_parts.extend(all_errors)
        error_text = "; ".join(error_parts) if error_parts else None

        elapsed = time.time() - start_time
        return BenchmarkResult(
            status=status,
            score=score,
            metrics=all_metrics,
            workload_results=workload_results,
            details=details,
            error=error_text,
            output_dir=output_dir,
            elapsed_sec=elapsed,
        )

    def parse_results(self, output: str) -> Dict[str, Any]:
        return {}

    def planned_workload_count(self, **kwargs) -> int:
        tier = str(kwargs.get("tier") or "").strip()
        cfg = self._get_config(kwargs)
        suites = self._select_suites(cfg, tier=tier)
        count = 0
        if "cispa" in suites:
            count += len(self._planned_cispa_rule_ids(cfg.cispa_mode))
        if "tfb" in suites:
            tests = cfg.tfb_tests or self._default_tfb_tests(tier)
            count += len(tests) if tests else 2
        if "h1spec" in suites:
            count += 33
        return max(count, 1)

    def planned_workload_ids(self, **kwargs) -> List[str]:
        tier = str(kwargs.get("tier") or "").strip()
        cfg = self._get_config(kwargs)
        suites = self._select_suites(cfg, tier=tier)
        ids: List[str] = []

        if "cispa" in suites:
            ids.extend(
                f"http_bench:cispa:{rule_id}"
                for rule_id in self._planned_cispa_rule_ids(cfg.cispa_mode)
            )

        if "tfb" in suites:
            tests = cfg.tfb_tests or self._default_tfb_tests(tier)
            ids.extend(f"http_bench:tfb:{test_name}" for test_name in tests)

        if "h1spec" in suites:
            ids.extend(
                f"http_bench:h1spec:case_{index:03d}"
                for index in range(1, 34)
            )

        return ids

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "http_bench": {
                "network_mode": "host",
                "cispa_repo": "https://github.com/cispa/http-conformance.git",
                "cispa_timeout_sec": 120,
                "cispa_postgres_image": "postgres:15-alpine",
                "tfb_timeout_sec": 300,
                "h1spec_repo": "https://github.com/uNetworking/h1spec",
                "h1spec_deno_image": "denoland/deno:alpine-2.1.4",
                "h1spec_script_url": "https://raw.githubusercontent.com/uNetworking/h1spec/master/http_test.ts",
                "h1spec_timeout_sec": 120,
                "suites": [],
            }
        }

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------

    def _get_config(self, kwargs: Dict[str, Any]) -> HttpBenchConfig:
        cfg = kwargs.get("http_bench")
        if not isinstance(cfg, dict):
            cfg = self.config.get("http_bench")
        if not isinstance(cfg, dict):
            cfg = {}

        def _get(key: str, default: Any) -> Any:
            if key in cfg:
                return cfg[key]
            return self.config.get(key, default)

        suites_raw = _get("suites", [])
        if isinstance(suites_raw, list):
            suites = [str(s).strip().lower() for s in suites_raw if str(s).strip()]
        else:
            suites = []

        tfb_tests_raw = _get("tfb_tests", [])
        if isinstance(tfb_tests_raw, list):
            tfb_tests = [str(s).strip().lower() for s in tfb_tests_raw if str(s).strip()]
        else:
            tfb_tests = []

        return HttpBenchConfig(
            network_mode=str(_get("network_mode", "host")),
            cispa_repo=str(_get("cispa_repo", "https://github.com/cispa/http-conformance.git")),
            cispa_timeout_sec=int(_get("cispa_timeout_sec", 120)),
            cispa_mode=str(_get("cispa_mode", "core_subset")),
            cispa_postgres_image=str(_get("cispa_postgres_image", "postgres:15-alpine")),
            cispa_postgres_startup_sec=int(_get("cispa_postgres_startup_sec", 30)),
            tfb_repo=str(_get("tfb_repo", "https://github.com/TechEmpower/FrameworkBenchmarks.git")),
            tfb_timeout_sec=int(_get("tfb_timeout_sec", 300)),
            tfb_tests=tfb_tests,
            h1spec_repo=str(_get("h1spec_repo", "https://github.com/uNetworking/h1spec")),
            h1spec_deno_image=str(_get("h1spec_deno_image", "denoland/deno:alpine-2.1.4")),
            h1spec_script_url=str(
                _get(
                    "h1spec_script_url",
                    "https://raw.githubusercontent.com/uNetworking/h1spec/master/http_test.ts",
                )
            ),
            h1spec_timeout_sec=int(_get("h1spec_timeout_sec", 120)),
            suites=suites,
        )

    def _select_suites(self, config: HttpBenchConfig, tier: str) -> List[str]:
        """Return the list of suite names to run for the given tier."""
        if config.suites:
            return list(dict.fromkeys(config.suites))

        tier_key = (tier or "").strip().upper()
        if tier_key == "L0":
            return ["h1spec"]
        if tier_key == "L1":
            return ["cispa"]
        if tier_key in {"L2", "L3", "L4"}:
            return ["tfb"]
        # Default: h1spec
        return ["h1spec"]

    def _default_tfb_tests(self, tier: str) -> List[str]:
        """Return default TFB test types for a given tier."""
        tier_key = (tier or "").strip().upper()
        if tier_key == "L2":
            return ["plaintext", "json"]
        if tier_key == "L3":
            return ["db", "query"]
        if tier_key == "L4":
            return ["fortune", "update"]
        return ["plaintext", "json"]

    @staticmethod
    def _planned_cispa_rule_ids(mode: str) -> List[str]:
        mode_key = str(mode or "").strip().lower()
        core_ids = list(CISPA_CURATED_CORE_RULES)
        if mode_key == "full":
            extra_ids = [
                f"cispa_full_rule_{index:03d}"
                for index in range(1, (CISPA_FULL_POINTS - CISPA_CORE_POINTS) + 1)
            ]
            return core_ids + extra_ids
        return core_ids

    @staticmethod
    def _remaining_timeout(deadline: float) -> int:
        """Return whole-second timeout budget remaining until the shared deadline."""
        remaining = deadline - time.time()
        if remaining <= 0:
            return 0
        return max(1, math.ceil(remaining))

    @staticmethod
    def _mark_pending_timeouts(
        workload_results: Dict[str, str],
        metrics: Dict[str, Any],
        pending_workloads: List[str],
        *,
        error: str,
    ) -> None:
        """Mark workloads that never started because the benchmark budget was exhausted."""
        for wid in pending_workloads:
            workload_results[wid] = "TIMEOUT"
            metrics[wid] = {
                "passed": False,
                "error": error,
            }

    @staticmethod
    def _status_from_shell_result(result: Dict[str, Any]) -> str:
        if result.get("error") == "timeout":
            return "TIMEOUT"
        return "PASS" if result.get("returncode") == 0 else "FAIL"

    @staticmethod
    def _is_timeout_text(detail: Optional[str]) -> bool:
        text = (detail or "").strip().lower()
        return "timeout" in text or "timed out" in text

    # ------------------------------------------------------------------
    # Shell / Docker helpers
    # ------------------------------------------------------------------

    def _run_shell(
        self,
        cmd: Union[str, List[str]],
        log_path: Path,
        timeout_sec: int,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[Path] = None,
    ) -> Dict[str, Any]:
        if isinstance(cmd, str):
            cmd_list = ["bash", "-lc", cmd]
        else:
            cmd_list = list(cmd)

        result: Dict[str, Any] = {
            "command": cmd if isinstance(cmd, str) else " ".join(cmd_list),
            "returncode": -1,
            "output": "",
            "error": None,
        }

        log_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            proc = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                cwd=str(cwd) if cwd else None,
            )
            try:
                stdout, _ = proc.communicate(timeout=timeout_sec)
                result["output"] = stdout or ""
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, _ = proc.communicate()
                result["output"] = (stdout or "") + "\n[TIMEOUT]\n"
                result["error"] = "timeout"
            result["returncode"] = proc.returncode
        except Exception as e:
            result["error"] = str(e)

        log_path.write_text(result["output"], encoding="utf-8")
        return result

    def _docker_usable(self, timeout_sec: int = 10) -> Tuple[bool, str]:
        if self._docker_probe is not None:
            return self._docker_probe

        if shutil.which("docker") is None:
            self._docker_probe = (False, "docker CLI not found in PATH")
            return self._docker_probe

        try:
            probe = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=max(1, timeout_sec),
            )
            if probe.returncode == 0:
                self._docker_probe = (True, "")
                return self._docker_probe

            combined = (probe.stderr or "") + "\n" + (probe.stdout or "")
            combined = combined.strip() or "docker info failed"
            self._docker_probe = (False, combined)
            return self._docker_probe
        except Exception as e:
            self._docker_probe = (False, str(e))
            return self._docker_probe

    def _build_docker_cmd(
        self,
        image: str,
        cmd_args: str,
        network_mode: str = "host",
    ) -> List[str]:
        cmd: List[str] = ["docker", "run", "--rm"]
        if network_mode == "host":
            cmd += ["--network", "host"]
        else:
            cmd += ["--add-host", "host.docker.internal:host-gateway"]
        cmd += [image]
        cmd += cmd_args.split()
        return cmd

    def _get_container_host(self, host: str, network_mode: str) -> str:
        if network_mode == "host":
            return host
        if host in ("127.0.0.1", "localhost"):
            return "host.docker.internal"
        return host

    @staticmethod
    def _find_free_port(host: str = "127.0.0.1") -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, 0))
            return int(s.getsockname()[1])

    def _ensure_docker_image(self, image: str, timeout_sec: int = 1800) -> Tuple[bool, str]:
        deadline = time.time() + max(0, timeout_sec)
        inspect_timeout = max(1, min(30, self._remaining_timeout(deadline)))
        try:
            inspect = subprocess.run(
                ["docker", "image", "inspect", image],
                capture_output=True,
                text=True,
                timeout=inspect_timeout,
            )
        except subprocess.TimeoutExpired:
            return False, "timeout while inspecting docker image"

        if inspect.returncode == 0:
            return True, ""

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            return False, "timeout while preparing docker image"

        try:
            pull = subprocess.run(
                ["docker", "pull", image],
                capture_output=True,
                text=True,
                timeout=remaining,
            )
        except subprocess.TimeoutExpired:
            return False, "timeout while pulling docker image"
        if pull.returncode == 0:
            return True, ""
        detail = (pull.stderr or pull.stdout or "").strip() or "docker pull failed"
        return False, detail

    def _start_cispa_postgres_container(
        self,
        *,
        image: str,
        startup_timeout_sec: int,
        timeout_sec: Optional[int] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str], bool]:
        deadline = None
        if timeout_sec is not None:
            deadline = time.time() + max(0, timeout_sec)

        docker_timeout = 10
        if deadline is not None:
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                return None, "benchmark timeout exhausted before cispa PostgreSQL startup", True
            docker_timeout = max(1, min(10, remaining))

        if deadline is not None and docker_timeout <= 0:
            return None, "benchmark timeout exhausted before cispa PostgreSQL startup", True

        docker_ok, docker_err = self._docker_usable(timeout_sec=docker_timeout)
        if not docker_ok:
            return None, f"Docker not usable for cispa PostgreSQL: {docker_err}", self._is_timeout_text(docker_err)

        image_timeout = 1800 if deadline is None else self._remaining_timeout(deadline)
        if deadline is not None and image_timeout <= 0:
            return None, "benchmark timeout exhausted before cispa PostgreSQL image prep", True

        image_ok, image_err = self._ensure_docker_image(image, timeout_sec=image_timeout)
        if not image_ok:
            return None, f"Unable to prepare PostgreSQL image {image}: {image_err}", self._is_timeout_text(image_err)

        host_port = self._find_free_port("127.0.0.1")
        container_name = (
            f"longagent-cispa-pg-{os.getpid()}-{int(time.time() * 1000)}-{host_port}"
        )
        run_cmd = [
            "docker", "run", "-d", "--rm",
            "--name", container_name,
            "-e", "POSTGRES_USER=postgres",
            "-e", "POSTGRES_PASSWORD=postgres",
            "-e", "POSTGRES_DB=postgres",
            "-p", f"127.0.0.1:{host_port}:5432",
            image,
        ]
        run_timeout = 60
        if deadline is not None:
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                return None, "benchmark timeout exhausted before starting cispa PostgreSQL container", True
            run_timeout = max(1, min(60, remaining))

        try:
            started = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                timeout=run_timeout,
            )
        except subprocess.TimeoutExpired:
            return None, "timeout while starting cispa PostgreSQL container", True
        if started.returncode != 0:
            detail = (started.stderr or started.stdout or "").strip() or "docker run failed"
            return None, f"Failed to start cispa PostgreSQL container: {detail}", False

        startup_budget = max(5, int(startup_timeout_sec))
        if deadline is not None:
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._stop_cispa_postgres_container({"container_name": container_name})
                return None, "benchmark timeout exhausted while waiting for cispa PostgreSQL", True
            startup_budget = min(startup_budget, remaining)
        startup_deadline = time.time() + max(1, int(startup_budget))
        last_detail = ""
        while time.time() < startup_deadline:
            probe_timeout = 10
            if deadline is not None:
                remaining = self._remaining_timeout(deadline)
                if remaining <= 0:
                    self._stop_cispa_postgres_container({"container_name": container_name})
                    return None, "benchmark timeout exhausted while waiting for cispa PostgreSQL", True
                probe_timeout = max(1, min(10, remaining, math.ceil(startup_deadline - time.time())))
            try:
                probe = subprocess.run(
                    ["docker", "exec", container_name, "pg_isready", "-U", "postgres"],
                    capture_output=True,
                    text=True,
                    timeout=probe_timeout,
                )
            except subprocess.TimeoutExpired:
                self._stop_cispa_postgres_container({"container_name": container_name})
                return None, "timeout while probing cispa PostgreSQL readiness", True
            if probe.returncode == 0:
                runtime = {
                    "container_name": container_name,
                    "image": image,
                    "env": {
                        "PGHOST": "127.0.0.1",
                        "PGPORT": str(host_port),
                        "PGUSER": "postgres",
                        "PGPASSWORD": "postgres",
                    },
                }
                return runtime, None, False
            last_detail = (probe.stderr or probe.stdout or "").strip()
            time.sleep(1)

        self._stop_cispa_postgres_container({"container_name": container_name})
        return None, (
            "cispa PostgreSQL container did not become ready in time"
            + (f": {last_detail}" if last_detail else "")
        ), True

    @staticmethod
    def _stop_cispa_postgres_container(runtime: Dict[str, Any]) -> None:
        name = str(runtime.get("container_name") or "").strip()
        if not name:
            return
        try:
            subprocess.run(
                ["docker", "rm", "-f", name],
                capture_output=True,
                text=True,
                timeout=20,
            )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Suite A: cispa/http-conformance
    # ------------------------------------------------------------------

    def _ensure_cispa_repo(self, cache_dir: Path, repo_url: str, timeout_sec: int = 120) -> Path:
        """Clone or reuse the cispa/http-conformance git repo."""
        if self._cispa_repo_dir and self._cispa_repo_dir.is_dir():
            return self._cispa_repo_dir

        deadline = time.time() + max(0, timeout_sec)
        repo_dir = cache_dir / "http_conformance_repo"
        if repo_dir.is_dir() and (repo_dir / ".git").is_dir():
            try:
                subprocess.run(
                    ["git", "pull", "--ff-only"],
                    cwd=str(repo_dir),
                    capture_output=True,
                    timeout=max(1, min(60, self._remaining_timeout(deadline))),
                )
            except Exception:
                pass
            self._cispa_repo_dir = repo_dir
            return repo_dir

        repo_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(repo_dir)],
            capture_output=True,
            timeout=max(1, self._remaining_timeout(deadline)),
            check=True,
        )
        self._cispa_repo_dir = repo_dir
        return repo_dir

    def _run_cispa_suite(
        self,
        host: str,
        port: int,
        config: HttpBenchConfig,
        raw_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run cispa/http-conformance tests, return (workload_results, metrics)."""
        cispa_raw = raw_dir / "cispa"
        cispa_raw.mkdir(parents=True, exist_ok=True)

        workload_results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}
        selected_rule_ids = list(self._planned_cispa_rule_ids(config.cispa_mode))

        if self._remaining_timeout(deadline) <= 0:
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error="benchmark timeout exhausted before cispa suite start",
                source="suite_setup",
            )
            return workload_results, metrics

        try:
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._mark_all_cispa_rules(
                    selected_rule_ids,
                    workload_results,
                    metrics,
                    status="TIMEOUT",
                    error="benchmark timeout exhausted before cispa repo setup",
                    source="suite_setup",
                )
                return workload_results, metrics
            repo_dir = self._ensure_cispa_repo(raw_dir.parent, config.cispa_repo, timeout_sec=remaining)
        except subprocess.TimeoutExpired:
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error="timeout while preparing cispa repo",
                source="suite_setup",
            )
            return workload_results, metrics
        except Exception as e:
            logger.error("Failed to clone cispa repo: %s", e)
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="RUNTIME_ERROR",
                error=f"Failed to clone cispa repo: {e}",
                source="suite_setup",
            )
            metrics["runtime_error"] = True
            metrics["error"] = f"Failed to clone cispa repo: {e}"
            return workload_results, metrics

        selected_rule_ids = self._expected_cispa_rule_ids(repo_dir, config.cispa_mode) or selected_rule_ids
        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error="benchmark timeout exhausted before cispa dependency install",
                source="suite_setup",
            )
            return workload_results, metrics

        dep_ok, dep_err = self._install_cispa_dependencies(repo_dir, timeout_sec=remaining)
        if not dep_ok:
            failed_status = "TIMEOUT" if self._is_timeout_text(dep_err) else "RUNTIME_ERROR"
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status=failed_status,
                error=dep_err or "Failed to install cispa dependencies",
                source="suite_setup",
            )
            if failed_status == "RUNTIME_ERROR":
                metrics["runtime_error"] = True
            metrics["error"] = dep_err or "Failed to install cispa dependencies"
            return workload_results, metrics
        if not selected_rule_ids:
            workload_results["cispa:all"] = "RUNTIME_ERROR"
            metrics["runtime_error"] = True
            metrics["error"] = "No CISPA rules selected for execution"
            return workload_results, metrics

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error="benchmark timeout exhausted before cispa adapter startup",
                source="suite_setup",
            )
            return workload_results, metrics

        pg_runtime, pg_err, pg_timed_out = self._start_cispa_postgres_container(
            image=config.cispa_postgres_image,
            startup_timeout_sec=config.cispa_postgres_startup_sec,
            timeout_sec=remaining,
        )
        if pg_timed_out:
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error=pg_err or "cispa PostgreSQL startup timed out",
                source="postgres_startup",
            )
            metrics["error"] = pg_err or "cispa PostgreSQL startup timed out"
            return workload_results, metrics
        if pg_err or not pg_runtime:
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="RUNTIME_ERROR",
                error=pg_err or "cispa PostgreSQL startup failed",
                source="postgres_startup",
            )
            metrics["runtime_error"] = True
            metrics["error"] = pg_err or "cispa PostgreSQL startup failed"
            return workload_results, metrics

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._stop_cispa_postgres_container(pg_runtime)
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error="benchmark timeout exhausted before cispa adapter execution",
                source="adapter",
            )
            return workload_results, metrics

        try:
            result, adapter_payload = self._run_cispa_adapter(
                repo_dir=repo_dir,
                host=(host or "").strip() or "127.0.0.1",
                port=port,
                raw_dir=cispa_raw,
                selected_rule_ids=selected_rule_ids,
                timeout_sec=max(1, min(remaining, config.cispa_timeout_sec)),
                pg_env=dict(pg_runtime["env"]),
            )
        finally:
            self._stop_cispa_postgres_container(pg_runtime)

        metrics["adapter_mode"] = "structured_local"
        metrics["postgres"] = {
            "mode": "docker_ephemeral",
            "image": config.cispa_postgres_image,
            "host": pg_runtime["env"]["PGHOST"],
            "port": pg_runtime["env"]["PGPORT"],
        }
        metrics["returncode"] = result["returncode"]

        if result.get("error") == "timeout":
            self._mark_all_cispa_rules(
                selected_rule_ids,
                workload_results,
                metrics,
                status="TIMEOUT",
                error="cispa adapter timed out",
                source="adapter",
            )
            metrics["error"] = "cispa adapter timed out"
            return workload_results, metrics

        if adapter_payload:
            metrics["db_name"] = adapter_payload.get("db_name")
            metrics["reqresp_count"] = adapter_payload.get("reqresp_count", 0)
            metrics["table_counts"] = adapter_payload.get("table_counts", {})
            metrics["cispa_materialized_rules"] = adapter_payload.get("materialized_rule_count", 0)

        rule_payloads: Dict[str, Any] = {}
        if adapter_payload and isinstance(adapter_payload.get("rule_results"), dict):
            rule_payloads = {
                self._sanitize_rule_id(rule_id): payload
                for rule_id, payload in adapter_payload["rule_results"].items()
                if self._sanitize_rule_id(rule_id)
            }

        missing_rule_ids: List[str] = []
        for rule_id in selected_rule_ids:
            wid = f"cispa:{rule_id}"
            rule_info = rule_payloads.get(rule_id)
            if not isinstance(rule_info, dict):
                missing_rule_ids.append(rule_id)
                workload_results[wid] = "RUNTIME_ERROR"
                metrics[wid] = {
                    "passed": False,
                    "error": "missing cispa rule result",
                    "source": "missing_expected_rule",
                }
                continue

            status = str(rule_info.get("status") or "RUNTIME_ERROR").strip().upper()
            if status not in {"PASS", "FAIL", "RUNTIME_ERROR", "TIMEOUT", "SKIP"}:
                status = "RUNTIME_ERROR"
            workload_results[wid] = status
            metrics[wid] = {
                "passed": status == "PASS",
                "source": str(rule_info.get("source") or "adapter"),
                "activity": rule_info.get("activity"),
                "reason": rule_info.get("reason"),
                "row_count": int(rule_info.get("row_count") or 0),
            }
            if rule_info.get("violations"):
                metrics[wid]["violations"] = list(rule_info.get("violations") or [])

        metrics["cispa_expected_rules"] = len(selected_rule_ids)
        if adapter_payload and adapter_payload.get("runtime_error"):
            metrics["runtime_error"] = True
            metrics["error"] = str(adapter_payload.get("runtime_error"))
        elif result["returncode"] != 0:
            metrics["runtime_error"] = True
            metrics["error"] = (
                str(result.get("output") or result.get("error") or "cispa adapter failed").strip()
            )

        if missing_rule_ids:
            metrics["runtime_error"] = True
            missing_msg = (
                "cispa adapter missing results for "
                f"{len(missing_rule_ids)}/{len(selected_rule_ids)} expected rule(s)"
            )
            if metrics.get("error"):
                metrics["error"] = f"{metrics['error']}; {missing_msg}"
            else:
                metrics["error"] = missing_msg

        if result.get("error") and not metrics.get("error"):
            metrics["error"] = result["error"]

        total = len(workload_results)
        passed_count = sum(1 for v in workload_results.values() if v == "PASS")
        logger.info("  cispa: %d/%d rules passed", passed_count, total)

        return workload_results, metrics

    @staticmethod
    def _mark_all_cispa_rules(
        rule_ids: List[str],
        workload_results: Dict[str, str],
        metrics: Dict[str, Any],
        *,
        status: str,
        error: str,
        source: str,
    ) -> None:
        targets = rule_ids or ["all"]
        for rule_id in targets:
            wid = f"cispa:{rule_id}"
            workload_results[wid] = status
            metrics[wid] = {
                "passed": status == "PASS",
                "error": error,
                "source": source,
            }
        metrics["cispa_expected_rules"] = len(targets)

    def _run_cispa_adapter(
        self,
        *,
        repo_dir: Path,
        host: str,
        port: int,
        raw_dir: Path,
        selected_rule_ids: List[str],
        timeout_sec: int,
        pg_env: Dict[str, str],
    ) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
        adapter_script = Path(__file__).with_name("http_bench_cispa_adapter.py")
        selected_rules_file = raw_dir / "selected_rules.json"
        output_json = raw_dir / "adapter_results.json"
        mitmdump_log = raw_dir / "mitmdump.log"
        selected_rules_file.write_text(
            json.dumps(selected_rule_ids, indent=2),
            encoding="utf-8",
        )

        env = os.environ.copy()
        env.update(pg_env)
        cmd = [
            sys.executable,
            str(adapter_script),
            "--repo-dir",
            str(repo_dir),
            "--host",
            host,
            "--port",
            str(port),
            "--selected-rules-json",
            str(selected_rules_file),
            "--output-json",
            str(output_json),
            "--mitmdump-log",
            str(mitmdump_log),
            "--probe-sleep",
            "0",
            "--direct-sleep",
            "0",
        ]
        result = self._run_shell(
            cmd,
            raw_dir / "cispa_run.log",
            timeout_sec=timeout_sec,
            env=env,
            cwd=PROJECT_ROOT,
        )

        payload: Optional[Dict[str, Any]] = None
        if output_json.exists():
            try:
                payload = json.loads(output_json.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning("Failed to load CISPA adapter output %s: %s", output_json, e)
        return result, payload

    @staticmethod
    def _is_cispa_cli_host_port_error(output: str) -> bool:
        text = (output or "").lower()
        if "unrecognized arguments" not in text:
            return False
        return ("--host" in text) or ("--port" in text)

    @staticmethod
    def _is_local_host(host: str) -> bool:
        return (host or "").strip().lower() in {"127.0.0.1", "localhost", "::1"}

    def _prepare_cispa_local_mode_repo(
        self,
        repo_dir: Path,
        host: str,
        port: int,
        pg_env: Optional[Dict[str, str]] = None,
    ) -> Optional[str]:
        if not self._is_local_host(host):
            return (
                "cispa local-mode adapter only supports localhost targets "
                f"(got host={host!r})"
            )

        testbed_dir = repo_dir / "testbed"
        if not testbed_dir.is_dir():
            return f"cispa local-mode adapter requires testbed directory: {testbed_dir}"

        env_file = testbed_dir / ".env"
        env_text = (
            "# Generated by LongAgentBench cispa adapter\n"
            f"target_http_port={port}\n"
        )
        env_file.write_text(env_text, encoding="utf-8")

        if pg_env:
            repo_env_file = repo_dir / ".env"
            repo_env_lines = ["# Generated by LongAgentBench cispa adapter"]
            for key in ("PGHOST", "PGPORT", "PGUSER", "PGPASSWORD"):
                value = pg_env.get(key)
                if value is not None:
                    repo_env_lines.append(f"{key}={value}")
            repo_env_file.write_text("\n".join(repo_env_lines) + "\n", encoding="utf-8")
        return None

    @staticmethod
    def _is_cispa_postgres_unavailable(output: str) -> bool:
        text = (output or "").lower()
        markers = (
            "psycopg2.operationalerror",
            "connection to server on socket",
            ".s.pgsql.5432",
            "database must be initialized before opening a connection",
        )
        return any(marker in text for marker in markers)

    def _parse_cispa_output(self, output: str) -> Dict[str, bool]:
        """Parse cispa/http-conformance output to extract per-rule results."""
        results: Dict[str, bool] = {}
        for line in output.splitlines():
            line = line.strip()
            # Try to parse lines like "RULE_ID: PASS" or "RULE_ID: FAIL"
            if ": PASS" in line.upper():
                parts = line.split(":")
                if len(parts) >= 2:
                    rule_id = parts[0].strip()
                    if rule_id:
                        results[rule_id] = True
            elif ": FAIL" in line.upper():
                parts = line.split(":")
                if len(parts) >= 2:
                    rule_id = parts[0].strip()
                    if rule_id:
                        results[rule_id] = False
        # Also try JSON output
        if not results:
            try:
                data = json.loads(output)
                if isinstance(data, dict):
                    for rule_id, info in data.items():
                        if isinstance(info, dict) and "result" in info:
                            results[rule_id] = info["result"].upper() in ("PASS", "OK", "TRUE")
                        elif isinstance(info, bool):
                            results[rule_id] = info
            except (json.JSONDecodeError, ValueError):
                pass
        return results

    @staticmethod
    def _sanitize_rule_id(rule_id: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(rule_id or "").strip())
        return cleaned.strip("._")

    def _load_core_rules(self, repo_dir: Path) -> Optional[List[str]]:
        """Load the core rule subset from benchmarks/rulesets/cispa_core_rules.txt."""
        candidates = [
            repo_dir / "benchmarks" / "rulesets" / "cispa_core_rules.txt",
            BENCHMARK_RULESET_DIR / "cispa_core_rules.txt",
        ]
        rules_file = next((path for path in candidates if path.exists()), None)
        if rules_file is None:
            return list(CISPA_CURATED_CORE_RULES)
        try:
            rules: List[str] = []
            seen: set[str] = set()
            for line in rules_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    rid = self._sanitize_rule_id(line)
                    if not rid or rid in seen:
                        continue
                    seen.add(rid)
                    rules.append(rid)
            return rules if rules else list(CISPA_CURATED_CORE_RULES)
        except Exception as e:
            logger.warning("Failed to load core rules: %s", e)
            return list(CISPA_CURATED_CORE_RULES)

    def _extract_cispa_rule_ids(self, repo_dir: Path) -> Tuple[List[str], List[str]]:
        """Extract cispa testcase IDs from testcases.py as (all_ids, requirement_ids)."""
        testcases_file = repo_dir / "testcases.py"
        if not testcases_file.exists():
            return [], []

        try:
            source = testcases_file.read_text(encoding="utf-8", errors="replace")
            with warnings.catch_warnings():
                # Upstream CISPA testcases contain invalid backslash escapes in
                # descriptive docstrings. They are irrelevant to rule discovery,
                # so suppress the resulting SyntaxWarning noise here.
                warnings.filterwarnings(
                    "ignore",
                    message=r"invalid escape sequence",
                    category=SyntaxWarning,
                )
                module = ast.parse(source)
        except Exception as e:
            logger.warning("Failed to parse cispa testcases.py: %s", e)
            return [], []

        all_ids: List[str] = []
        requirement_ids: List[str] = []
        seen: set[str] = set()

        for node in module.body:
            if not isinstance(node, ast.ClassDef):
                continue

            level_value: Optional[str] = None
            for stmt in node.body:
                if not isinstance(stmt, ast.Assign):
                    continue
                for target in stmt.targets:
                    if not isinstance(target, ast.Name) or target.id != "type":
                        continue
                    value = stmt.value
                    if (
                        isinstance(value, ast.Attribute)
                        and isinstance(value.value, ast.Name)
                        and value.value.id == "Level"
                    ):
                        level_value = value.attr

            rule_id = self._sanitize_rule_id(node.name)
            if not rule_id or rule_id in seen:
                continue
            seen.add(rule_id)
            all_ids.append(rule_id)
            if level_value == "REQUIREMENT":
                requirement_ids.append(rule_id)

        return all_ids, requirement_ids

    def _normalize_rule_ids(
        self,
        candidates: List[str],
        *,
        target_size: int,
        fallback_prefix: str,
    ) -> List[str]:
        out: List[str] = []
        seen: set[str] = set()

        for rid in candidates:
            clean = self._sanitize_rule_id(rid)
            if not clean or clean in seen:
                continue
            seen.add(clean)
            out.append(clean)
            if len(out) >= target_size:
                return out

        i = 1
        while len(out) < target_size:
            rid = f"{fallback_prefix}_{i:03d}"
            i += 1
            if rid in seen:
                continue
            seen.add(rid)
            out.append(rid)
        return out

    def _expected_cispa_rule_ids(self, repo_dir: Path, mode: str) -> List[str]:
        mode_key = str(mode or "").strip().lower()
        all_ids, requirement_ids = self._extract_cispa_rule_ids(repo_dir)
        if mode_key == "core_subset":
            core_rules = self._load_core_rules(repo_dir)
            if core_rules:
                return self._normalize_rule_ids(
                    core_rules,
                    target_size=len(core_rules),
                    fallback_prefix="cispa_core_rule",
                )
            base = requirement_ids or all_ids
            return self._normalize_rule_ids(
                base,
                target_size=CISPA_CORE_POINTS,
                fallback_prefix="cispa_core_rule",
            )

        base = all_ids or requirement_ids
        return self._normalize_rule_ids(
            base,
            target_size=CISPA_FULL_POINTS,
            fallback_prefix="cispa_full_rule",
        )

    @staticmethod
    def _infer_import_name(package_name: str) -> str:
        name = package_name.strip().lower().replace("-", "_")
        overrides = {
            "python_dotenv": "dotenv",
            "pyyaml": "yaml",
            "jinja2": "jinja2",
            "scikit_learn": "sklearn",
            "psycopg2_binary": "psycopg2",
            "strenum": "strenum",
        }
        return overrides.get(name, name)

    @staticmethod
    def _to_pip_spec(pkg_name: str, requirement: Any) -> str:
        def _apply_version(base: str, version_text: str) -> str:
            v = version_text.strip()
            if not v or v == "*":
                return base
            if v.startswith("^") or v.startswith("~"):
                return f"{base}>={v[1:]}"
            if v.startswith((">", "<", "=", "!")):
                return f"{base}{v}"
            return f"{base}=={v}"

        if isinstance(requirement, str):
            return _apply_version(pkg_name, requirement)

        if isinstance(requirement, dict):
            extras = requirement.get("extras")
            base = pkg_name
            if isinstance(extras, list) and extras:
                extras_text = ",".join(str(x).strip() for x in extras if str(x).strip())
                if extras_text:
                    base = f"{base}[{extras_text}]"
            version = requirement.get("version")
            if isinstance(version, str):
                return _apply_version(base, version)
            return base

        return pkg_name

    def _extract_poetry_dependency_specs(self, pyproject_file: Path, timeout_sec: int = 300) -> List[Tuple[str, str]]:
        toml_loader = self._ensure_toml_loader(timeout_sec=timeout_sec)
        if toml_loader is None:
            return []

        try:
            raw = toml_loader.loads(pyproject_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Failed to parse cispa pyproject.toml: %s", e)
            return []

        tool = raw.get("tool") or {}
        poetry = tool.get("poetry") or {}
        deps = poetry.get("dependencies") or {}
        if not isinstance(deps, dict):
            return []

        specs: List[Tuple[str, str]] = []
        for pkg_name, requirement in deps.items():
            raw_name = str(pkg_name).strip()
            if not raw_name or raw_name.lower() == "python":
                continue
            pip_name = "psycopg2-binary" if raw_name.lower() == "psycopg2" else raw_name
            pip_spec = self._to_pip_spec(pip_name, requirement)
            import_name = self._infer_import_name(pip_name)
            specs.append((pip_spec, import_name))
        return specs

    def _ensure_toml_loader(self, timeout_sec: int = 300) -> Any:
        global tomllib
        if tomllib is not None:
            return tomllib

        try:
            import tomli as toml_loader  # type: ignore[import-not-found]
            tomllib = toml_loader
            return tomllib
        except Exception:
            pass

        # Best-effort bootstrap when running on Python < 3.11.
        install = subprocess.run(
            [sys.executable, "-m", "pip", "install", "tomli"],
            capture_output=True,
            text=True,
            timeout=max(1, timeout_sec),
        )
        if install.returncode != 0:
            logger.warning(
                "Unable to install tomli for parsing pyproject.toml: %s",
                (install.stderr or install.stdout or "").strip(),
            )
            return None
        try:
            import tomli as toml_loader  # type: ignore[import-not-found]
            tomllib = toml_loader
            return tomllib
        except Exception as e:
            logger.warning("Unable to import tomli after installation: %s", e)
            return None

    @staticmethod
    def _python_version() -> Tuple[int, int]:
        return (sys.version_info.major, sys.version_info.minor)

    @classmethod
    def _resolve_runtime_compatible_spec(cls, spec: str) -> str:
        match = re.match(
            r"^\s*([A-Za-z0-9_.-]+)(\[[^\]]+\])?\s*(==|>=|<=|!=|~=|>|<)?\s*(.*?)\s*$",
            spec,
        )
        if not match:
            return spec
        pkg, extras, op, version_text = match.group(1), match.group(2), match.group(3), match.group(4)
        pkg_key = pkg.lower()

        if pkg_key == "pandas":
            if cls._python_version() < (3, 13):
                return spec
            if op != "==":
                return spec

            parsed = cls._parse_major_minor(version_text)
            if parsed is None or parsed >= (2, 2):
                return spec
            return f"{pkg}{extras or ''}>=2.2.0"

        if pkg_key == "mitmproxy":
            if cls._python_version() < (3, 12):
                return spec
            parsed = cls._parse_major_minor(version_text)
            if parsed is None:
                return spec
            if parsed < (10, 2):
                # mitmproxy 8.x does not start correctly on Python 3.12 in our
                # benchmark environment; prefer the nearest newer major line.
                return f"{pkg}{extras or ''}>=10.2.1,<11"

        return spec

    @staticmethod
    def _parse_major_minor(version_text: str) -> Optional[Tuple[int, int]]:
        m = re.match(r"^\s*(\d+)(?:\.(\d+))?", version_text or "")
        if not m:
            return None
        return (int(m.group(1)), int(m.group(2) or "0"))

    def _install_cispa_dependencies(self, repo_dir: Path, timeout_sec: int = 600) -> Tuple[bool, Optional[str]]:
        """Install cispa dependencies from requirements.txt or pyproject.toml."""
        deadline = time.time() + max(0, timeout_sec)
        req_file = repo_dir / "requirements.txt"
        if req_file.exists():
            try:
                remaining = self._remaining_timeout(deadline)
                if remaining <= 0:
                    return False, "benchmark timeout exhausted before cispa dependency install"
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                    capture_output=True,
                    text=True,
                    timeout=remaining,
                )
                if result.returncode != 0:
                    detail = (result.stderr or result.stdout or "").strip()
                    return False, f"pip install -r requirements.txt failed: {detail}"
                return True, None
            except subprocess.TimeoutExpired:
                return False, "timeout while installing cispa requirements.txt dependencies"
            except Exception as e:
                return False, f"Failed to install cispa requirements.txt deps: {e}"

        pyproject_file = repo_dir / "pyproject.toml"
        if not pyproject_file.exists():
            return False, f"No requirements.txt or pyproject.toml found in {repo_dir}"

        specs = self._extract_poetry_dependency_specs(pyproject_file, timeout_sec=max(1, self._remaining_timeout(deadline)))
        if not specs:
            return False, "Unable to extract cispa dependencies from pyproject.toml"

        for spec, import_name in specs:
            try:
                install_spec = self._resolve_runtime_compatible_spec(spec)
                module_exists = importlib.util.find_spec(import_name) is not None
                if module_exists and install_spec == spec:
                    continue
                remaining = self._remaining_timeout(deadline)
                if remaining <= 0:
                    return False, "benchmark timeout exhausted while installing cispa dependencies"
                if install_spec != spec:
                    logger.info(
                        "Adjusting dependency for current Python runtime: %s -> %s",
                        spec,
                        install_spec,
                    )
                logger.info("Installing missing cispa dependency: %s", install_spec)
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", install_spec],
                    capture_output=True,
                    text=True,
                    timeout=remaining,
                )
                if result.returncode != 0:
                    detail = (result.stderr or result.stdout or "").strip()
                    return False, f"pip install {install_spec} failed: {detail}"
            except subprocess.TimeoutExpired:
                return False, f"timeout while installing cispa dependency {spec}"
            except Exception as e:
                return False, f"Failed to install cispa dependency {spec}: {e}"

        return True, None

    # ------------------------------------------------------------------
    # Suite B: TFB correctness verification
    # ------------------------------------------------------------------

    def _run_tfb_suite(
        self,
        host: str,
        port: int,
        config: HttpBenchConfig,
        raw_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run TFB correctness verification tests, return (workload_results, metrics)."""
        tfb_raw = raw_dir / "tfb"
        tfb_raw.mkdir(parents=True, exist_ok=True)

        workload_results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        test_types = config.tfb_tests
        if not test_types:
            test_types = ["plaintext", "json"]

        if self._remaining_timeout(deadline) <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [f"tfb:{test_type}" for test_type in test_types],
                error="benchmark timeout exhausted before tfb suite start",
            )
            return workload_results, metrics

        target_host = (host or "").strip() or "127.0.0.1"
        base_url = f"http://{target_host}:{port}"

        # TFB verification endpoints and expected behavior
        tfb_endpoints = {
            "plaintext": {
                "url": f"{base_url}/plaintext",
                "content_type": "text/plain",
                "expected_body": "Hello, World!",
            },
            "json": {
                "url": f"{base_url}/json",
                "content_type": "application/json",
                "expected_json": {"message": "Hello, World!"},
            },
            "db": {
                "url": f"{base_url}/db",
                "content_type": "application/json",
                "validate": "db_single",
            },
            "query": {
                "url": f"{base_url}/queries?queries=5",
                "content_type": "application/json",
                "validate": "db_multi",
            },
            "fortune": {
                "url": f"{base_url}/fortunes",
                "content_type": "text/html",
                "validate": "fortune",
            },
            "update": {
                "url": f"{base_url}/updates?queries=5",
                "content_type": "application/json",
                "validate": "db_multi",
            },
        }

        for index, test_type in enumerate(test_types):
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._mark_pending_timeouts(
                    workload_results,
                    metrics,
                    [f"tfb:{pending}" for pending in test_types[index:]],
                    error="benchmark timeout exhausted before workload start",
                )
                break
            if test_type not in tfb_endpoints:
                workload_results[f"tfb:{test_type}"] = "FAIL"
                metrics[f"tfb:{test_type}"] = {"error": f"Unknown test type: {test_type}"}
                continue

            endpoint = tfb_endpoints[test_type]
            log_path = tfb_raw / f"tfb_{test_type}.log"

            status, details = self._verify_tfb_endpoint(
                endpoint,
                test_type,
                log_path,
                max(1, min(remaining, config.tfb_timeout_sec)),
            )

            wid = f"tfb:{test_type}"
            workload_results[wid] = status
            metrics[wid] = {
                "passed": status == "PASS",
                "details": details,
            }
            logger.info("  %s: %s", wid, status)

        return workload_results, metrics

    def _verify_tfb_endpoint(
        self,
        endpoint: Dict[str, Any],
        test_type: str,
        log_path: Path,
        timeout_sec: int,
    ) -> Tuple[str, str]:
        """Verify a single TFB endpoint. Returns (status, details)."""
        import urllib.request
        import urllib.error

        url = endpoint["url"]
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("Accept", "*/*")
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                status = resp.status
                headers = {k.lower(): v for k, v in resp.getheaders()}
                body = resp.read().decode("utf-8", errors="replace")
        except urllib.error.URLError as e:
            details = f"Connection error: {e}"
            log_path.write_text(details, encoding="utf-8")
            is_timeout = isinstance(getattr(e, "reason", None), TimeoutError) or self._is_timeout_text(str(e))
            return ("TIMEOUT" if is_timeout else "FAIL"), details
        except Exception as e:
            details = f"Request error: {e}"
            log_path.write_text(details, encoding="utf-8")
            return ("TIMEOUT" if self._is_timeout_text(str(e)) else "FAIL"), details

        errors: List[str] = []
        log_lines: List[str] = [
            f"URL: {url}",
            f"Status: {status}",
            f"Headers: {headers}",
            f"Body (first 500): {body[:500]}",
            "",
        ]

        # Common checks: Server and Date headers
        if "server" not in headers:
            errors.append("Missing Server header")
        if "date" not in headers:
            errors.append("Missing Date header")

        # Status check
        if status != 200:
            errors.append(f"Expected status 200, got {status}")

        # Content-Type check
        expected_ct = endpoint.get("content_type", "")
        actual_ct = headers.get("content-type", "")
        if expected_ct and expected_ct not in actual_ct:
            errors.append(f"Content-Type mismatch: expected '{expected_ct}' in '{actual_ct}'")

        # Body checks per test type
        if "expected_body" in endpoint:
            if body.strip() != endpoint["expected_body"]:
                errors.append(f"Body mismatch: expected '{endpoint['expected_body']}', got '{body.strip()[:100]}'")

        if "expected_json" in endpoint:
            try:
                parsed = json.loads(body)
                expected = endpoint["expected_json"]
                if parsed != expected:
                    errors.append(f"JSON mismatch: expected {expected}, got {parsed}")
            except json.JSONDecodeError as e:
                errors.append(f"Invalid JSON: {e}")

        if "validate" in endpoint:
            validate_type = endpoint["validate"]
            if validate_type == "db_single":
                self._validate_db_single(body, errors)
            elif validate_type == "db_multi":
                self._validate_db_multi(body, errors)
            elif validate_type == "fortune":
                self._validate_fortune(body, errors)

        if errors:
            log_lines.append("ERRORS:")
            log_lines.extend(f"  - {e}" for e in errors)
        else:
            log_lines.append("PASS")

        log_path.write_text("\n".join(log_lines), encoding="utf-8")
        return ("PASS" if not errors else "FAIL"), "; ".join(errors) if errors else "OK"

    def _validate_db_single(self, body: str, errors: List[str]) -> None:
        """Validate TFB single DB query response."""
        try:
            obj = json.loads(body)
            if not isinstance(obj, dict):
                errors.append("DB response should be a JSON object")
                return
            if "id" not in obj:
                errors.append("Missing 'id' field")
            if "randomNumber" not in obj and "randomnumber" not in obj:
                errors.append("Missing 'randomNumber' field")
            # Check value ranges
            id_val = obj.get("id")
            rn_val = obj.get("randomNumber") or obj.get("randomnumber")
            if isinstance(id_val, int) and not (1 <= id_val <= 10000):
                errors.append(f"id out of range: {id_val}")
            if isinstance(rn_val, int) and not (1 <= rn_val <= 10000):
                errors.append(f"randomNumber out of range: {rn_val}")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")

    def _validate_db_multi(self, body: str, errors: List[str]) -> None:
        """Validate TFB multiple DB queries response."""
        try:
            arr = json.loads(body)
            if not isinstance(arr, list):
                errors.append("Multi-query response should be a JSON array")
                return
            if len(arr) == 0:
                errors.append("Empty response array")
                return
            for i, obj in enumerate(arr[:5]):  # Check first 5
                if not isinstance(obj, dict):
                    errors.append(f"Element {i} is not a JSON object")
                    continue
                if "id" not in obj:
                    errors.append(f"Element {i}: missing 'id'")
                if "randomNumber" not in obj and "randomnumber" not in obj:
                    errors.append(f"Element {i}: missing 'randomNumber'")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")

    def _validate_fortune(self, body: str, errors: List[str]) -> None:
        """Validate TFB fortune response (basic checks)."""
        if "<table" not in body.lower():
            errors.append("Missing <table> element")
        if "Additional fortune added at request time" not in body:
            errors.append("Missing dynamically added fortune")
        if "&lt;script&gt;" not in body and "<script>" in body:
            errors.append("Script tag not properly escaped (XSS vulnerability)")

    # ------------------------------------------------------------------
    # Suite C: h1spec
    # ------------------------------------------------------------------

    def _run_h1spec_suite(
        self,
        host: str,
        port: int,
        config: HttpBenchConfig,
        raw_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run h1spec HTTP/1.1 conformance tests, return (workload_results, metrics)."""
        h1_raw = raw_dir / "h1spec"
        h1_raw.mkdir(parents=True, exist_ok=True)

        wid = "h1spec:all"
        target_host = (host or "").strip() or "127.0.0.1"
        log_path = h1_raw / "h1spec_all.log"
        h1spec_bin = shutil.which("h1spec")

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            return {wid: "TIMEOUT"}, {
                wid: {
                    "returncode": -1,
                    "error": "benchmark timeout exhausted before h1spec suite start",
                }
            }

        if h1spec_bin is None:
            docker_ok, docker_err = self._docker_usable(timeout_sec=max(1, min(10, remaining)))
            if not docker_ok:
                status = "TIMEOUT" if self._is_timeout_text(docker_err) else "FAIL"
                return {wid: status}, {
                    wid: {
                        "returncode": -1,
                        "error": (
                            "h1spec not found. Install h1spec from "
                            f"{config.h1spec_repo} or provide Docker ({docker_err})."
                        ),
                    }
                }
            container_host = self._get_container_host(target_host, config.network_mode)
            cmd = self._build_docker_cmd(
                config.h1spec_deno_image,
                f"run --allow-net {config.h1spec_script_url} {container_host} {port}",
                config.network_mode,
            )
        else:
            cmd = [h1spec_bin, "-h", target_host, "-p", str(port)]

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            return {wid: "TIMEOUT"}, {
                wid: {
                    "returncode": -1,
                    "error": "benchmark timeout exhausted before h1spec execution",
                }
            }

        effective_timeout = max(1, min(remaining, config.h1spec_timeout_sec))
        result = self._run_shell(cmd, log_path, timeout_sec=effective_timeout)
        if result.get("error") == "timeout":
            return {wid: "TIMEOUT"}, {
                wid: {
                    "command": result.get("command"),
                    "returncode": result.get("returncode"),
                    "error": "timeout",
                }
            }

        output = result.get("output", "")
        test_results = self._parse_h1spec_output(output)
        metrics: Dict[str, Any] = {}
        workload_results: Dict[str, str] = {}

        if test_results:
            for test_name, passed in test_results.items():
                wid_test = f"h1spec:{test_name}"
                workload_results[wid_test] = "PASS" if passed else "FAIL"
                metrics[wid_test] = {"passed": passed}
        else:
            # Do not award PASS when h1spec output is not parseable.
            fallback_error = result.get("error")
            if result.get("returncode") == 0 and not fallback_error:
                fallback_error = "h1spec produced no parseable test results"
            workload_results[wid] = "FAIL"
            metrics[wid] = {
                "command": result.get("command"),
                "returncode": result.get("returncode"),
                "error": fallback_error,
            }

        return workload_results, metrics

    @staticmethod
    def _parse_h1spec_output(output: str) -> Dict[str, bool]:
        """Parse h1spec output to extract individual test results.

        Looks for lines like:
          ✅ <test name>: ...
          ❌ <test name>: ...
          PASS: <test name>
          FAIL: <test name>
          ok <N> - <test name>
          not ok <N> - <test name>
        """
        results: Dict[str, bool] = {}
        name_counts: Dict[str, int] = {}
        if not output:
            return results

        ansi = re.compile(r"\x1b\[[0-9;]*m")

        def _store(raw_name: str, passed: bool) -> None:
            name = (raw_name or "").strip()
            if not name:
                return
            count = name_counts.get(name, 0) + 1
            name_counts[name] = count
            key = name if count == 1 else f"{name} #{count}"
            results[key] = passed

        for line in output.splitlines():
            line = ansi.sub("", line).strip()
            m = re.match(r"^([✅❌])\s+(.+?):\s+.+$", line)
            if m:
                _store(m.group(2), m.group(1) == "✅")
                continue
            # Format: "PASS: test name" / "FAIL: test name"
            m = re.match(r"^(PASS|FAIL):\s+(.+)$", line, re.IGNORECASE)
            if m:
                status, name = m.group(1).upper(), m.group(2).strip()
                _store(name, status == "PASS")
                continue
            # TAP format: "ok 1 - test name" / "not ok 1 - test name"
            m = re.match(r"^(not\s+)?ok\s+\d+\s+-\s+(.+)$", line, re.IGNORECASE)
            if m:
                failed = m.group(1) is not None
                name = m.group(2).strip()
                _store(name, not failed)

        return results

    # ------------------------------------------------------------------
    # Error helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _first_workload_error(
        metrics: Dict[str, Any], failures: List[str]
    ) -> Optional[str]:
        """Return the error string from the first failed workload, if any."""
        for wid in failures:
            entry = metrics.get(wid)
            if isinstance(entry, dict):
                err = entry.get("error") or entry.get("details")
                if err:
                    return str(err)[:200]
        return None

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _calculate_score(self, workload_results: Dict[str, str]) -> float:
        """Score = fraction of passed workloads."""
        if not workload_results:
            return 0.0
        passed = sum(1 for v in workload_results.values() if v == "PASS")
        return passed / len(workload_results)


from ..registry import register_benchmark

register_benchmark("http_bench", HttpBenchRunner)
