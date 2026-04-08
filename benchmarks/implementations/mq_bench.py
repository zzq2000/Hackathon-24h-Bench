"""
Message Queue Benchmark Runner Implementation

Runs AMQP 0.9.1 benchmarks against message queue implementations.

Three benchmark suites, mapped to progressive tiers:
  - pika:     Pika library acceptance tests (protocol correctness)
  - omq:      pivotalrabbitmq/omq Docker-based throughput/latency tests
  - perftest: pivotalrabbitmq/perf-test Docker-based heavy performance tests

Fallback tier mapping when no per-tier suites are configured:
  L0/tier0 → pika only
  L1/tier1 → pika + omq
  L2/tier2 → pika + omq + perftest
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import select
import shlex
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..base import BenchmarkResult, BenchmarkRunner, BenchmarkStatus

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pika test groups: each entry is (workload_id, pytest -k filter expression)
# ---------------------------------------------------------------------------
PIKA_TEST_GROUPS: List[Tuple[str, str]] = [
    (
        "pika:connection",
        "TestCreateAndCloseConnection or TestMultiCloseConnection or TestConnectionContextManager",
    ),
    ("pika:channel", "TestCreateAndCloseChannel"),
    ("pika:queue_declare", "TestQueueDeclareAndDelete or TestPassiveQueueDeclare"),
    ("pika:exchange_declare", "TestExchangeDeclareAndDelete"),
    ("pika:exchange_bind", "TestExchangeBindAndUnbind"),
    ("pika:queue_bind", "TestQueueBindAndUnbindAndPurge"),
    ("pika:basic_publish", "TestBasicPublishWithoutPubacks"),
    (
        "pika:basic_consume",
        "TestPublishAndConsumeWithPubacksAndQosOfOne or TestTwoBasicConsumersOnSameChannel or TestPublishFromBasicConsumeCallback",
    ),
    ("pika:basic_get", "TestBasicGet"),
    ("pika:basic_reject", "TestBasicReject or TestBasicNack"),
    (
        "pika:publisher_confirms",
        "TestConfirmDelivery or TestPublishAndBasicPublishWithPubacks or TestUnroutableMessage",
    ),
    ("pika:tx", "TestTxCommit or TestTxRollback"),
    ("pika:basic_recover", "TestBasicRecoverWithRequeue"),
    (
        "pika:consume_cancel",
        "TestBasicCancelPurges or TestStopConsumingFromBasicConsumeCallback",
    ),
    ("pika:process_data_events", "TestProcessDataEvents or TestSleep"),
    ("pika:callback_threadsafe", "TestAddCallbackThreadsafe"),
]

# ---------------------------------------------------------------------------
# OMQ test definitions: (workload_id, extra_args)
# ---------------------------------------------------------------------------
OMQ_TESTS: List[Tuple[str, str]] = [
    ("omq:basic", "--publishers 1 --consumers 1 --rate 100 --size 256 -z 10s"),
    ("omq:throughput", "--publishers 2 --consumers 2 --rate 5000 --size 256 -z 15s"),
    ("omq:latency", "--publishers 1 --consumers 1 --rate 100 --size 64 -z 10s"),
    ("omq:multi_pub", "--publishers 4 --consumers 1 --rate 1000 --size 256 -z 10s"),
    ("omq:multi_con", "--publishers 1 --consumers 4 --rate 1000 --size 256 -z 10s"),
    ("omq:payload", "--publishers 1 --consumers 1 --rate 500 --size 4096 -z 10s"),
]

# ---------------------------------------------------------------------------
# PerfTest test definitions: (workload_id, extra_args)
# ---------------------------------------------------------------------------
PERFTEST_TESTS: List[Tuple[str, str]] = [
    ("perftest:baseline", "-x 1 -y 1 --size 1024 -z 30"),
    ("perftest:multi_pub", "-x 4 -y 1 --size 1024 -z 30"),
    ("perftest:multi_con", "-x 1 -y 4 --size 1024 -z 30"),
    ("perftest:persistent", "-x 1 -y 1 --size 1024 -z 30 -f persistent"),
    ("perftest:confirm", "-x 1 -y 1 --size 1024 -z 30 --confirm 1"),
    ("perftest:exchange_fanout", "-x 1 -y 2 --size 1024 -z 30 -t fanout"),
    ("perftest:payload", "-x 1 -y 1 --size 8192 -z 30"),
    ("perftest:latency", "-x 1 -y 1 --size 256 -z 30 --use-millis"),
]

SUPPORTED_SUITES: Tuple[str, ...] = ("pika", "omq", "perftest")

OMQ_DEFAULT_ADDRESS = "/queues/omq-%d"
OMQ_FATAL_OUTPUT_MARKERS: Tuple[str, ...] = (
    "Queue not found:",
    "channel/connection is not open",
    "SASL could not negotiate a shared mechanism",
)
OMQ_DURATION_RE = re.compile(r"^(?P<value>\d+)(?P<unit>[smh])$")
OMQ_TIMEOUT_GRACE_SEC = 15
OMQ_SAMPLE_RATE_RE = re.compile(
    r"published=(?P<published>[0-9.]+)/s\s+consumed=(?P<consumed>[0-9.]+)/s"
)
OMQ_TOTAL_PUBLISHED_RE = re.compile(
    r"TOTAL PUBLISHED messages=(?P<count>[0-9]+)\s+confirmed=[0-9]+\s+returned=[0-9]+\s+rate=(?P<rate>[0-9.]+)/s"
)
OMQ_TOTAL_CONSUMED_RE = re.compile(
    r"TOTAL CONSUMED messages=(?P<count>[0-9]+)\s+rate=(?P<rate>[0-9.]+)/s"
)
OMQ_MIN_ACTIVE_SAMPLE_COUNT = 5
OMQ_MAX_ZERO_CONSUME_RATIO = 0.5
OMQ_MIN_CONSUME_TO_PUBLISH_RATIO = 0.1
OMQ_MAX_CONSUME_TO_PUBLISH_RATIO = 1.5
OMQ_CONTAINER_NAME_PREFIX = "lab-mq-bench-omq"

PERFTEST_PARSE_FAILURE_MARKERS: Tuple[str, ...] = (
    "Parsing failed.",
    "Unrecognized option:",
)
PERFTEST_CONFIRM_RATE_RE = re.compile(r"confirmed:\s*([0-9.]+)\s+msg/s")
PERFTEST_SAMPLE_RATE_RE = re.compile(
    r"sent:\s*(?P<sent>[0-9.]+)\s+msg/s.*?received:\s*(?P<received>[0-9.]+)\s+msg/s"
)
PERFTEST_SENDING_RATE_AVG_RE = re.compile(
    r"sending rate avg:\s*(?P<rate>[0-9.]+)\s+msg/s"
)
PERFTEST_RECEIVING_RATE_AVG_RE = re.compile(
    r"receiving rate avg:\s*(?P<rate>[0-9.]+)\s+msg/s"
)
PERFTEST_MIN_ACTIVE_SAMPLE_COUNT = 5
PERFTEST_MAX_ZERO_RECEIVE_RATIO = 0.5
PERFTEST_MIN_RECEIVE_TO_SEND_RATIO = 0.05
PERFTEST_MAX_RECEIVE_TO_SEND_RATIO = 1.5
PROTOCOL_ERROR_PATTERNS: Tuple[re.Pattern[str], ...] = (
    re.compile(r"\bUnexpectedFrameError\b", re.IGNORECASE),
    re.compile(r"\bFRAME_ERROR\b", re.IGNORECASE),
    re.compile(r"\bunknown frame type\b", re.IGNORECASE),
    re.compile(r"\bmethod frame too short\b", re.IGNORECASE),
    re.compile(r"\bheader frame too short\b", re.IGNORECASE),
    re.compile(r"\bcontent header on channel 0\b", re.IGNORECASE),
    re.compile(r"\bcontent body on channel 0\b", re.IGNORECASE),
    re.compile(r"\binvalid frame end\b", re.IGNORECASE),
    re.compile(r"\bmalformed frame\b", re.IGNORECASE),
)


@dataclass
class MQBenchConfig:
    """Configuration for the AMQP 0.9.1 benchmark runner."""

    network_mode: str = "host"
    pika_repo: str = "https://github.com/pika/pika.git"
    pika_test_timeout_sec: int = 30
    omq_docker_image: str = "pivotalrabbitmq/omq"
    perftest_docker_image: str = "pivotalrabbitmq/perf-test"
    suites: List[str] = field(default_factory=list)


class MessageQueueBenchRunner(BenchmarkRunner):
    """AMQP 0.9.1 benchmark runner (pika / omq / perftest)."""

    name = "mq_bench"
    description = "AMQP 0.9.1 MQ benchmark (pika acceptance, OMQ, PerfTest)"
    supported_suts = ["message_queue"]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._docker_probe: Optional[Tuple[bool, str]] = None
        self._pika_repo_dir: Optional[Path] = None

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
        unknown_suites = sorted({suite for suite in suites if suite not in SUPPORTED_SUITES})
        if unknown_suites:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error=(
                    f"Unsupported mq_bench suite(s): {', '.join(unknown_suites)}. "
                    f"Supported suites: {', '.join(SUPPORTED_SUITES)}"
                ),
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )
        if not suites:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error="No enabled suites in mq_bench config",
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )

        workload_results: Dict[str, str] = {}
        all_metrics: Dict[str, Any] = {}
        all_errors: List[str] = []

        if "pika" in suites:
            logger.info("Running mq_bench suite: pika")
            pika_results, pika_metrics = self._run_pika_suite(
                sut_host, sut_port, bench_config, raw_dir, benchmark_deadline
            )
            workload_results.update(pika_results)
            all_metrics["pika"] = pika_metrics
            pika_failures = [k for k, v in pika_results.items() if v != "PASS"]
            if pika_failures:
                err_summary = f"pika: {len(pika_failures)} test group(s) failed"
                first_err = self._first_workload_error(pika_metrics, pika_failures)
                if first_err:
                    err_summary += f" (first error: {first_err})"
                all_errors.append(err_summary)

        if "omq" in suites:
            logger.info("Running mq_bench suite: omq")
            omq_results, omq_metrics = self._run_omq_suite(
                sut_host, sut_port, bench_config, raw_dir, benchmark_deadline
            )
            workload_results.update(omq_results)
            all_metrics["omq"] = omq_metrics
            omq_failures = [k for k, v in omq_results.items() if v != "PASS"]
            if omq_failures:
                err_summary = f"omq: {len(omq_failures)} test(s) failed"
                first_err = self._first_workload_error(omq_metrics, omq_failures)
                if first_err:
                    err_summary += f" (first error: {first_err})"
                all_errors.append(err_summary)

        if "perftest" in suites:
            logger.info("Running mq_bench suite: perftest")
            pt_results, pt_metrics = self._run_perftest_suite(
                sut_host, sut_port, bench_config, raw_dir, benchmark_deadline
            )
            workload_results.update(pt_results)
            all_metrics["perftest"] = pt_metrics
            pt_failures = [k for k, v in pt_results.items() if v != "PASS"]
            if pt_failures:
                err_summary = f"perftest: {len(pt_failures)} test(s) failed"
                first_err = self._first_workload_error(pt_metrics, pt_failures)
                if first_err:
                    err_summary += f" (first error: {first_err})"
                all_errors.append(err_summary)

        non_pass = {status for status in workload_results.values() if status not in {"PASS", "SKIP"}}
        if not non_pass:
            status = BenchmarkStatus.ACCEPTED
        elif non_pass <= {"TIMEOUT"}:
            status = BenchmarkStatus.TIME_LIMIT_EXCEEDED
        else:
            status = BenchmarkStatus.WRONG_ANSWER
        score = self._calculate_score(workload_results)

        # Persist results
        (output_dir / "mq_bench_results.json").write_text(
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

        elapsed = time.time() - start_time
        return BenchmarkResult(
            status=status,
            score=score,
            metrics=all_metrics,
            workload_results=workload_results,
            details=(
                f"MQ Bench: {'; '.join(all_errors)}"
                if all_errors
                else "All suites passed"
            ),
            error="; ".join(all_errors) if all_errors else None,
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
        if "pika" in suites:
            count += len(PIKA_TEST_GROUPS)
        if "omq" in suites:
            count += len(OMQ_TESTS)
        if "perftest" in suites:
            count += len(PERFTEST_TESTS)
        return max(count, 1)

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "mq_bench": {
                "network_mode": "host",
                "pika_repo": "https://github.com/pika/pika.git",
                "pika_test_timeout_sec": 30,
                "omq_docker_image": "pivotalrabbitmq/omq",
                "perftest_docker_image": "pivotalrabbitmq/perf-test",
                "suites": [],
            }
        }

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------

    def _get_config(self, kwargs: Dict[str, Any]) -> MQBenchConfig:
        cfg = kwargs.get("mq_bench")
        if not isinstance(cfg, dict):
            cfg = self.config.get("mq_bench")
        if not isinstance(cfg, dict):
            cfg = {}

        def _get(key: str, default: Any) -> Any:
            if key in cfg:
                return cfg[key]
            return self.config.get(key, default)

        suites_raw = _get("suites", [])
        if isinstance(suites_raw, list):
            suites = [str(s).strip().lower() for s in suites_raw if str(s).strip()]
        elif isinstance(suites_raw, dict):
            # Legacy dict format — extract enabled suite names
            suites = [
                str(k).strip().lower()
                for k, v in suites_raw.items()
                if isinstance(v, dict) and v.get("enabled", True) and str(k).strip()
            ]
        else:
            suites = []

        return MQBenchConfig(
            network_mode=str(_get("network_mode", "host")),
            pika_repo=str(_get("pika_repo", "https://github.com/pika/pika.git")),
            pika_test_timeout_sec=int(_get("pika_test_timeout_sec", 30)),
            omq_docker_image=str(_get("omq_docker_image", "pivotalrabbitmq/omq")),
            perftest_docker_image=str(_get("perftest_docker_image", "pivotalrabbitmq/perf-test")),
            suites=suites,
        )

    def _select_suites(self, config: MQBenchConfig, tier: str) -> List[str]:
        """Return the list of suite names to run for the given tier."""
        # If config already has explicit suites, use them
        if config.suites:
            return list(dict.fromkeys(config.suites))

        tier_key = (tier or "").strip().lower()
        if tier_key in {"l0", "t0", "tier0"}:
            return ["pika"]
        if tier_key in {"l1", "t1", "tier1"}:
            return ["pika", "omq"]
        if tier_key in {"l2", "l3", "t2", "t3", "tier2", "tier3"}:
            return list(SUPPORTED_SUITES)
        # Default: pika only
        return ["pika"]

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
                "returncode": -1,
                "error": error,
            }

    @staticmethod
    def _status_from_shell_result(result: Dict[str, Any]) -> str:
        if result.get("error") == "timeout":
            return "TIMEOUT"
        return "PASS" if result.get("returncode") == 0 else "FAIL"

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

    def _run_omq_workload(
        self,
        cmd: Union[str, List[str]],
        log_path: Path,
        timeout_sec: int,
        container_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run OMQ with streaming log inspection so deterministic failures fail fast."""
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
        output_parts: List[str] = []

        log_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            proc = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            stdout = proc.stdout
            deadline = time.monotonic() + max(1, timeout_sec)
            if stdout is not None:
                while proc.poll() is None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        proc.kill()
                        result["error"] = "timeout"
                        break

                    ready, _, _ = select.select([stdout], [], [], min(0.2, remaining))
                    if not ready:
                        continue

                    line = stdout.readline()
                    if not line:
                        continue

                    output_parts.append(line)
                    fatal_error = self._find_omq_fatal_output_marker(line)
                    if fatal_error:
                        proc.kill()
                        if container_name:
                            self._remove_docker_container(container_name)
                        result["error"] = fatal_error
                        break

            remainder, _ = proc.communicate()
            if remainder:
                output_parts.append(remainder)

            result["returncode"] = proc.returncode
            result["output"] = "".join(output_parts)
            if result["error"] == "timeout":
                result["output"] += "\n[TIMEOUT]\n"
            elif result["error"]:
                result["output"] += "\n[FAIL-FAST]\n"
        except Exception as e:
            result["error"] = str(e)
        finally:
            if container_name:
                self._remove_docker_container(container_name)

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
        container_name: Optional[str] = None,
    ) -> List[str]:
        cmd: List[str] = ["docker", "run", "--rm"]
        if container_name:
            cmd += ["--name", container_name]
        if network_mode == "host":
            cmd += ["--network", "host"]
        else:
            cmd += ["--add-host", "host.docker.internal:host-gateway"]
        cmd += [image]
        cmd += cmd_args.split()
        return cmd

    @staticmethod
    def _omq_container_name(workload_id: str) -> str:
        safe_workload = re.sub(r"[^a-z0-9]+", "-", workload_id.lower()).strip("-")
        return f"{OMQ_CONTAINER_NAME_PREFIX}-{os.getpid()}-{int(time.time() * 1000)}-{safe_workload}"

    def _remove_docker_container(self, container_name: str, timeout_sec: int = 10) -> None:
        if not container_name:
            return
        try:
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                capture_output=True,
                text=True,
                timeout=max(1, timeout_sec),
                check=False,
            )
        except Exception:
            pass

    def _cleanup_stale_omq_containers(self, image: str, timeout_sec: int = 10) -> None:
        """Best-effort cleanup for leaked OMQ helper containers from prior failed runs."""
        try:
            result = subprocess.run(
                ["docker", "ps", "-aq", "--filter", f"ancestor={image}"],
                capture_output=True,
                text=True,
                timeout=max(1, timeout_sec),
                check=False,
            )
            container_ids = [
                line.strip() for line in (result.stdout or "").splitlines() if line.strip()
            ]
            for container_id in container_ids:
                self._remove_docker_container(container_id, timeout_sec=timeout_sec)
        except Exception:
            pass

    def _get_container_host(self, host: str, network_mode: str) -> str:
        if network_mode == "host":
            return host
        if host in ("127.0.0.1", "localhost"):
            return "host.docker.internal"
        return host

    # ------------------------------------------------------------------
    # Suite A: Pika acceptance tests
    # ------------------------------------------------------------------

    def _ensure_pika_repo(self, cache_dir: Path, timeout_sec: int = 120) -> Path:
        """Clone or reuse the pika git repo."""
        if self._pika_repo_dir and self._pika_repo_dir.is_dir():
            return self._pika_repo_dir

        repo_dir = cache_dir / "pika_repo"
        if repo_dir.is_dir() and (repo_dir / ".git").is_dir():
            # Pull latest
            try:
                subprocess.run(
                    ["git", "pull", "--ff-only"],
                    cwd=str(repo_dir),
                    capture_output=True,
                    timeout=max(1, min(60, timeout_sec)),
                )
            except Exception:
                pass
            self._pika_repo_dir = repo_dir
            return repo_dir

        repo_dir.mkdir(parents=True, exist_ok=True)
        pika_url = self.config.get("pika_repo", "https://github.com/pika/pika.git")
        subprocess.run(
            ["git", "clone", "--depth", "1", pika_url, str(repo_dir)],
            capture_output=True,
            timeout=max(1, timeout_sec),
            check=True,
        )
        self._pika_repo_dir = repo_dir
        return repo_dir

    def _ensure_pika_installed(self, timeout_sec: int = 120) -> bool:
        """Make sure the pika library is importable."""
        try:
            import pika as _pika  # noqa: F401
            return True
        except ImportError:
            pass
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pika"],
                capture_output=True,
                timeout=max(1, timeout_sec),
                check=True,
            )
            return True
        except Exception as e:
            logger.error("Failed to install pika: %s", e)
            return False

    def _run_pytest_group(
        self,
        repo_dir: Path,
        filter_expr: str,
        host: str,
        port: int,
        timeout_sec: int,
        log_path: Path,
    ) -> Dict[str, Any]:
        """Run a pytest -k filter against the pika blocking adapter tests."""
        test_file = repo_dir / "tests" / "acceptance" / "blocking_adapter_test.py"
        if not test_file.exists():
            return {
                "returncode": -1,
                "output": f"Test file not found: {test_file}",
                "error": "test file missing",
            }

        cmd = [
            sys.executable, "-m", "pytest",
            str(test_file),
            "-k", filter_expr,
            "-x",
            "-v",
        ]
        target_host = (host or "").strip() or "127.0.0.1"

        env = {
            **os.environ,
            "RABBITMQ_HOST": target_host,
            "RABBITMQ_PORT": str(port),
            # Some pika test setups use these env vars
            "PIKA_TEST_HOST": target_host,
            "PIKA_TEST_PORT": str(port),
        }

        return self._run_shell(cmd, log_path, timeout_sec=timeout_sec, env=env, cwd=repo_dir)

    def _write_pika_conftest(self, repo_dir: Path, host: str, port: int) -> None:
        """Write a conftest.py that overrides DEFAULT_URL with the actual port."""
        conftest_path = repo_dir / "tests" / "acceptance" / "conftest.py"
        conftest_content = (
            "# Auto-generated by mq_bench to override default connection params\n"
            "import importlib\n"
            "import os\n"
            "import pika\n"
            "\n"
            "_host = os.environ.get('RABBITMQ_HOST', '127.0.0.1')\n"
            "_port = os.environ.get('RABBITMQ_PORT', '5672')\n"
            "\n"
            "def _patch_module(_bat):\n"
            "    _template = _bat.PARAMS_URL_TEMPLATE.replace('127.0.0.1', _host)\n"
            "    _url = _template % {'port': int(_port)}\n"
            "    _bat.DEFAULT_URL = _url\n"
            "    _bat.DEFAULT_PARAMS = pika.URLParameters(_url)\n"
            "    # _connect(url=DEFAULT_URL, ...) captures default at function definition time.\n"
            "    _defaults = getattr(_bat.BlockingTestCaseBase._connect, '__defaults__', None)\n"
            "    if isinstance(_defaults, tuple) and _defaults:\n"
            "        _bat.BlockingTestCaseBase._connect.__defaults__ = (_url,) + _defaults[1:]\n"
            "\n"
            "for _name in ('acceptance.blocking_adapter_test', 'tests.acceptance.blocking_adapter_test'):\n"
            "    try:\n"
            "        _patch_module(importlib.import_module(_name))\n"
            "    except Exception:\n"
            "        pass\n"
        )
        conftest_path.write_text(conftest_content, encoding="utf-8")

    def _run_pika_suite(
        self,
        host: str,
        port: int,
        config: MQBenchConfig,
        raw_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run all pika test groups, return (workload_results, metrics)."""
        pika_raw = raw_dir / "pika"
        pika_raw.mkdir(parents=True, exist_ok=True)

        workload_results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        if self._remaining_timeout(deadline) <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in PIKA_TEST_GROUPS],
                error="benchmark timeout exhausted before pika suite start",
            )
            return workload_results, metrics

        # Ensure pika library is installed
        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in PIKA_TEST_GROUPS],
                error="benchmark timeout exhausted before pika dependency setup",
            )
            return workload_results, metrics

        if not self._ensure_pika_installed(timeout_sec=remaining):
            for wid, _ in PIKA_TEST_GROUPS:
                workload_results[wid] = "FAIL"
            metrics["error"] = "Failed to install pika library"
            return workload_results, metrics

        # Clone pika repo
        try:
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._mark_pending_timeouts(
                    workload_results,
                    metrics,
                    [wid for wid, _ in PIKA_TEST_GROUPS],
                    error="benchmark timeout exhausted before pika repo setup",
                )
                return workload_results, metrics
            repo_dir = self._ensure_pika_repo(raw_dir.parent, timeout_sec=remaining)
        except Exception as e:
            logger.error("Failed to clone pika repo: %s", e)
            for wid, _ in PIKA_TEST_GROUPS:
                workload_results[wid] = "FAIL"
            metrics["error"] = f"Failed to clone pika repo: {e}"
            return workload_results, metrics

        # Write conftest.py to override hardcoded port in pika tests
        try:
            self._write_pika_conftest(repo_dir, host, port)
        except Exception as e:
            logger.warning("Failed to write pika conftest.py: %s", e)

        for index, (wid, filter_expr) in enumerate(PIKA_TEST_GROUPS):
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._mark_pending_timeouts(
                    workload_results,
                    metrics,
                    [pending_wid for pending_wid, _ in PIKA_TEST_GROUPS[index:]],
                    error="benchmark timeout exhausted before workload start",
                )
                break
            log_path = pika_raw / f"{wid.replace(':', '_')}.log"
            group_timeout = max(1, min(config.pika_test_timeout_sec, remaining))
            result = self._run_pytest_group(
                repo_dir, filter_expr, host, port, group_timeout, log_path
            )
            protocol_error = self._find_protocol_error_marker(result.get("output", ""))
            status = self._status_from_shell_result(result)
            if protocol_error:
                status = "FAIL"
            passed = status == "PASS"
            error_snippet = protocol_error or result.get("error")
            if status == "FAIL" and not error_snippet:
                error_snippet = self._extract_pytest_error(result.get("output", ""))
            workload_results[wid] = status
            metrics[wid] = {
                "passed": passed,
                "returncode": result["returncode"],
                "error": error_snippet,
            }
            logger.info("  %s: %s", wid, status)

        return workload_results, metrics

    @staticmethod
    def _extract_pytest_error(output: str) -> Optional[str]:
        """Extract the key error line from pytest output."""
        if not output:
            return None
        # Look for the "E   <exception>" lines pytest produces
        for line in output.splitlines():
            stripped = line.strip()
            if stripped.startswith("E ") and (
                "Error" in stripped or "Exception" in stripped
                or "refused" in stripped.lower() or "timeout" in stripped.lower()
            ):
                return stripped[2:].strip()
        # Fallback: look for "FAILED" short summary line
        for line in output.splitlines():
            if line.strip().startswith("FAILED "):
                return line.strip()
        return None

    @staticmethod
    def _extract_shell_error(output: str) -> Optional[str]:
        """Extract the first meaningful line from failing shell output."""
        if not output:
            return None
        for line in output.splitlines():
            stripped = line.strip()
            if stripped and stripped != "[TIMEOUT]":
                return stripped
        return None

    # ------------------------------------------------------------------
    # Suite B: OMQ tests
    # ------------------------------------------------------------------

    def _run_omq_suite(
        self,
        host: str,
        port: int,
        config: MQBenchConfig,
        raw_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run OMQ Docker tests, return (workload_results, metrics)."""
        omq_raw = raw_dir / "omq"
        omq_raw.mkdir(parents=True, exist_ok=True)

        workload_results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        if self._remaining_timeout(deadline) <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in OMQ_TESTS],
                error="benchmark timeout exhausted before omq suite start",
            )
            return workload_results, metrics

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in OMQ_TESTS],
                error="benchmark timeout exhausted before omq docker probe",
            )
            return workload_results, metrics

        docker_ok, docker_err = self._docker_usable(timeout_sec=min(10, remaining))
        if not docker_ok:
            for wid, _ in OMQ_TESTS:
                workload_results[wid] = "FAIL"
            metrics["error"] = f"Docker not usable: {docker_err}"
            return workload_results, metrics

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in OMQ_TESTS],
                error="benchmark timeout exhausted before omq dependency setup",
            )
            return workload_results, metrics
        if not self._ensure_pika_installed(timeout_sec=min(30, remaining)):
            for wid, _ in OMQ_TESTS:
                workload_results[wid] = "FAIL"
            metrics["error"] = "Failed to install pika library"
            return workload_results, metrics

        self._cleanup_stale_omq_containers(config.omq_docker_image)

        omq_network_mode = config.network_mode
        container_host = self._get_container_host(host, omq_network_mode)
        uri = f"amqp://guest:guest@{container_host}:{port}/"

        for index, (wid, extra_args) in enumerate(OMQ_TESTS):
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._mark_pending_timeouts(
                    workload_results,
                    metrics,
                    [pending_wid for pending_wid, _ in OMQ_TESTS[index:]],
                    error="benchmark timeout exhausted before workload start",
                )
                break

            prepare_error = self._prepare_omq_queues(host, port, extra_args)
            if prepare_error:
                workload_results[wid] = "FAIL"
                metrics[wid] = {
                    "passed": False,
                    "returncode": -1,
                    "error": prepare_error,
                }
                logger.info("  %s: FAIL", wid)
                continue

            log_path = omq_raw / f"{wid.replace(':', '_')}.log"
            cmd_args = f"amqp091-amqp091 --uri {uri} {extra_args}"
            container_name = self._omq_container_name(wid)
            docker_cmd = self._build_docker_cmd(
                config.omq_docker_image,
                cmd_args,
                omq_network_mode,
                container_name=container_name,
            )
            workload_timeout = self._omq_workload_timeout(extra_args, remaining)
            result = self._run_omq_workload(
                docker_cmd,
                log_path,
                workload_timeout,
                container_name=container_name,
            )
            protocol_error = self._find_protocol_error_marker(result.get("output", ""))
            status = self._status_from_shell_result(result)
            validation_error = None
            if protocol_error:
                status = "FAIL"
            elif status == "PASS":
                validation_error = self._validate_omq_output(result.get("output", ""))
                if validation_error:
                    status = "FAIL"
            passed = status == "PASS"
            error_snippet = protocol_error or result.get("error") or validation_error
            if status == "FAIL" and not error_snippet:
                error_snippet = self._extract_shell_error(result.get("output", ""))
            workload_results[wid] = status
            metrics[wid] = {
                "passed": passed,
                "returncode": result["returncode"],
                "error": error_snippet,
            }
            logger.info("  %s: %s", wid, status)

        return workload_results, metrics

    # ------------------------------------------------------------------
    # Suite C: PerfTest tests
    # ------------------------------------------------------------------

    def _run_perftest_suite(
        self,
        host: str,
        port: int,
        config: MQBenchConfig,
        raw_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run PerfTest Docker tests, return (workload_results, metrics)."""
        pt_raw = raw_dir / "perftest"
        pt_raw.mkdir(parents=True, exist_ok=True)

        workload_results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        if self._remaining_timeout(deadline) <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in PERFTEST_TESTS],
                error="benchmark timeout exhausted before perftest suite start",
            )
            return workload_results, metrics

        remaining = self._remaining_timeout(deadline)
        if remaining <= 0:
            self._mark_pending_timeouts(
                workload_results,
                metrics,
                [wid for wid, _ in PERFTEST_TESTS],
                error="benchmark timeout exhausted before perftest docker probe",
            )
            return workload_results, metrics

        docker_ok, docker_err = self._docker_usable(timeout_sec=min(10, remaining))
        if not docker_ok:
            for wid, _ in PERFTEST_TESTS:
                workload_results[wid] = "FAIL"
            metrics["error"] = f"Docker not usable: {docker_err}"
            return workload_results, metrics

        container_host = self._get_container_host(host, config.network_mode)
        uri = f"amqp://{container_host}:{port}"

        for index, (wid, extra_args) in enumerate(PERFTEST_TESTS):
            remaining = self._remaining_timeout(deadline)
            if remaining <= 0:
                self._mark_pending_timeouts(
                    workload_results,
                    metrics,
                    [pending_wid for pending_wid, _ in PERFTEST_TESTS[index:]],
                    error="benchmark timeout exhausted before workload start",
                )
                break
            log_path = pt_raw / f"{wid.replace(':', '_')}.log"
            cmd_args = f"--uri {uri} {extra_args}"
            docker_cmd = self._build_docker_cmd(
                config.perftest_docker_image, cmd_args, config.network_mode
            )
            result = self._run_shell(docker_cmd, log_path, remaining)
            protocol_error = self._find_protocol_error_marker(result.get("output", ""))
            status = self._status_from_shell_result(result)
            validation_error = None
            if protocol_error:
                status = "FAIL"
            elif status == "PASS":
                validation_error = self._validate_perftest_output(
                    wid, result.get("output", "")
                )
                if validation_error:
                    status = "FAIL"
            passed = status == "PASS"
            error_snippet = protocol_error or result.get("error") or validation_error
            if status == "FAIL" and not error_snippet:
                error_snippet = self._extract_shell_error(result.get("output", ""))
            workload_results[wid] = status
            metrics[wid] = {
                "passed": passed,
                "returncode": result["returncode"],
                "error": error_snippet,
            }
            logger.info("  %s: %s", wid, status)

        return workload_results, metrics

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
            if isinstance(entry, dict) and entry.get("error"):
                return str(entry["error"])
        return None

    @staticmethod
    def _find_protocol_error_marker(output: str) -> Optional[str]:
        """Return the first obvious protocol/frame error line from benchmark output."""
        if not output:
            return None

        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            for pattern in PROTOCOL_ERROR_PATTERNS:
                if pattern.search(line):
                    return line
        return None

    @staticmethod
    def _validate_perftest_output(workload_id: str, output: str) -> Optional[str]:
        """Reject perf-test false positives that exit 0 without a valid workload run."""
        if not output.strip():
            return "perf-test produced no output"

        protocol_error = MessageQueueBenchRunner._find_protocol_error_marker(output)
        if protocol_error:
            return protocol_error

        lines = [line.strip() for line in output.splitlines() if line.strip()]
        first_line = lines[0] if lines else "perf-test output was empty"

        for marker in PERFTEST_PARSE_FAILURE_MARKERS:
            if marker in output:
                return first_line

        if "starting producer" not in output:
            return "perf-test did not start any producers"
        if "sending rate avg:" not in output or "receiving rate avg:" not in output:
            return "perf-test did not report throughput summary"

        sample_count = sum(
            1 for line in lines if ", time " in line and ", sent:" in line
        )
        if sample_count == 0:
            return "perf-test did not report any periodic samples"

        sample_rates = [
            (
                float(match.group("sent")),
                float(match.group("received")),
            )
            for line in lines
            if ", time " in line and ", sent:" in line
            for match in [PERFTEST_SAMPLE_RATE_RE.search(line)]
            if match is not None
        ]
        if len(sample_rates) != sample_count:
            return "perf-test reported unparseable producer/consumer samples"

        has_consumers = "starting consumer" in output
        sending_rate_avg = MessageQueueBenchRunner._parse_perftest_summary_rate(
            lines, PERFTEST_SENDING_RATE_AVG_RE
        )
        receiving_rate_avg = MessageQueueBenchRunner._parse_perftest_summary_rate(
            lines, PERFTEST_RECEIVING_RATE_AVG_RE
        )
        if sending_rate_avg is None or receiving_rate_avg is None:
            return "perf-test did not report parseable throughput summary"

        if has_consumers:
            if receiving_rate_avg <= 0.0:
                return "perf-test reported zero receiving throughput"

            active_samples = sample_rates[1:] if len(sample_rates) > 1 else sample_rates
            active_samples = [
                (sent_rate, recv_rate)
                for sent_rate, recv_rate in active_samples
                if sent_rate > 0.0
            ]
            if len(active_samples) >= PERFTEST_MIN_ACTIVE_SAMPLE_COUNT:
                zero_receive_ratio = (
                    sum(1 for _, recv_rate in active_samples if recv_rate == 0.0)
                    / len(active_samples)
                )
                if zero_receive_ratio > PERFTEST_MAX_ZERO_RECEIVE_RATIO:
                    return "perf-test consumers stalled for most of the run"

            if sending_rate_avg > 0.0:
                receive_ratio = receiving_rate_avg / sending_rate_avg
                if receive_ratio < PERFTEST_MIN_RECEIVE_TO_SEND_RATIO:
                    return (
                        "perf-test receive throughput too low relative to send "
                        f"throughput ({receiving_rate_avg:g}/{sending_rate_avg:g} msg/s)"
                    )
                # Fanout workloads legitimately multiply; non-fanout must not.
                is_fanout = "fanout" in workload_id
                upper = PERFTEST_MAX_RECEIVE_TO_SEND_RATIO
                if not is_fanout and receive_ratio > upper:
                    return (
                        "perf-test duplicate message delivery detected "
                        f"(receiving {receiving_rate_avg:g} > sending "
                        f"{sending_rate_avg:g} msg/s, ratio {receive_ratio:.1f}x)"
                    )

        if workload_id == "perftest:confirm":
            confirm_rates = [
                float(match.group(1))
                for line in lines
                for match in [PERFTEST_CONFIRM_RATE_RE.search(line)]
                if match is not None
            ]
            if not confirm_rates:
                return "perf-test confirm workload did not report confirm metrics"
            if max(confirm_rates) <= 0.0:
                return "perf-test confirm workload observed zero confirms"

        return None

    @staticmethod
    def _parse_perftest_summary_rate(
        lines: List[str], pattern: re.Pattern[str]
    ) -> Optional[float]:
        for line in reversed(lines):
            match = pattern.search(line)
            if match is not None:
                return float(match.group("rate"))
        return None

    @staticmethod
    def _omq_workload_timeout(extra_args: str, remaining: int) -> int:
        duration_sec = MessageQueueBenchRunner._extract_omq_duration_sec(extra_args)
        if duration_sec is None:
            return max(1, remaining)
        return max(1, min(remaining, duration_sec + OMQ_TIMEOUT_GRACE_SEC))

    @staticmethod
    def _extract_omq_duration_sec(extra_args: str) -> Optional[int]:
        tokens = shlex.split(extra_args)
        for index, token in enumerate(tokens):
            if token not in {"-z", "--time"} or index + 1 >= len(tokens):
                continue
            return MessageQueueBenchRunner._parse_omq_duration(tokens[index + 1])
        return None

    @staticmethod
    def _parse_omq_duration(value: str) -> Optional[int]:
        match = OMQ_DURATION_RE.match(value.strip())
        if not match:
            return None
        amount = int(match.group("value"))
        unit = match.group("unit")
        multipliers = {"s": 1, "m": 60, "h": 3600}
        return amount * multipliers[unit]

    @staticmethod
    def _validate_omq_output(output: str) -> Optional[str]:
        if not output.strip():
            return "omq produced no output"

        protocol_error = MessageQueueBenchRunner._find_protocol_error_marker(output)
        if protocol_error:
            return protocol_error

        lines = [line.strip() for line in output.splitlines() if line.strip()]
        fatal_error = MessageQueueBenchRunner._find_omq_fatal_output_marker(output)
        if fatal_error:
            return fatal_error

        if "publisher started" not in output:
            return "omq did not start any publishers"
        if "consumer started" not in output:
            return "omq did not start any consumers"

        sample_rates = [
            (
                float(match.group("published")),
                float(match.group("consumed")),
            )
            for line in lines
            for match in [OMQ_SAMPLE_RATE_RE.search(line)]
            if match is not None
        ]
        if not sample_rates:
            return "omq did not report any publish/consume samples"

        active_samples = [
            (published_rate, consumed_rate)
            for published_rate, consumed_rate in sample_rates
            if published_rate > 0.0
        ]
        if len(active_samples) >= OMQ_MIN_ACTIVE_SAMPLE_COUNT:
            zero_consume_ratio = (
                sum(1 for _, consumed_rate in active_samples if consumed_rate == 0.0)
                / len(active_samples)
            )
            if zero_consume_ratio > OMQ_MAX_ZERO_CONSUME_RATIO:
                return "omq consumers stalled for most of the run"

        published_total = MessageQueueBenchRunner._parse_omq_summary_value(
            lines, OMQ_TOTAL_PUBLISHED_RE
        )
        consumed_total = MessageQueueBenchRunner._parse_omq_summary_value(
            lines, OMQ_TOTAL_CONSUMED_RE
        )
        if published_total is None or consumed_total is None:
            return "omq did not report throughput summary"
        if published_total <= 0.0:
            return "omq reported zero published messages"
        if consumed_total <= 0.0:
            return "omq reported zero consumed messages"

        consume_ratio = consumed_total / published_total
        if consume_ratio < OMQ_MIN_CONSUME_TO_PUBLISH_RATIO:
            return (
                "omq receive throughput too low relative to publish throughput "
                f"({consumed_total:g}/{published_total:g} messages)"
            )
        if consume_ratio > OMQ_MAX_CONSUME_TO_PUBLISH_RATIO:
            return (
                "omq duplicate message delivery detected "
                f"(consumed {consumed_total:g} > published {published_total:g}, "
                f"ratio {consume_ratio:.1f}x)"
            )
        return None

    @staticmethod
    def _find_omq_fatal_output_marker(output: str) -> Optional[str]:
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            for marker in OMQ_FATAL_OUTPUT_MARKERS:
                if marker in line:
                    return line
        return None

    @staticmethod
    def _parse_omq_summary_value(
        lines: List[str], pattern: re.Pattern[str]
    ) -> Optional[float]:
        for line in reversed(lines):
            match = pattern.search(line)
            if match is not None:
                return float(match.group("count"))
        return None

    @staticmethod
    def _normalize_omq_queue_name(address: str) -> str:
        address = address.strip()
        if address.startswith("/queues/"):
            return address[len("/queues/") :]
        return address

    @staticmethod
    def _omq_queue_names(extra_args: str) -> List[str]:
        tokens = shlex.split(extra_args)
        publishers = 1
        consumers = 1
        publish_to = OMQ_DEFAULT_ADDRESS
        consume_from = OMQ_DEFAULT_ADDRESS

        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token in {"--publishers", "-x"} and index + 1 < len(tokens):
                publishers = int(tokens[index + 1])
                index += 2
                continue
            if token in {"--consumers", "-y"} and index + 1 < len(tokens):
                consumers = int(tokens[index + 1])
                index += 2
                continue
            if token in {"--publish-to", "-t"} and index + 1 < len(tokens):
                publish_to = tokens[index + 1]
                index += 2
                continue
            if token in {"--consume-from", "-T"} and index + 1 < len(tokens):
                consume_from = tokens[index + 1]
                index += 2
                continue
            index += 1

        queue_names = set()
        for publisher_id in range(1, publishers + 1):
            queue_names.add(
                MessageQueueBenchRunner._normalize_omq_queue_name(
                    publish_to.replace("%d", str(publisher_id))
                )
            )
        for consumer_id in range(1, consumers + 1):
            queue_names.add(
                MessageQueueBenchRunner._normalize_omq_queue_name(
                    consume_from.replace("%d", str(consumer_id))
                )
            )

        return sorted(name for name in queue_names if name)

    def _prepare_omq_queues(self, host: str, port: int, extra_args: str) -> Optional[str]:
        try:
            import pika

            timeout_sec = max(1, min(10, self._extract_omq_duration_sec(extra_args) or 10))
            deadline = time.monotonic() + timeout_sec
            last_error: Optional[Exception] = None

            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break

                attempt_timeout = max(1, min(3, int(math.ceil(remaining))))
                parameters = pika.ConnectionParameters(
                    host=host,
                    port=port,
                    virtual_host="/",
                    credentials=pika.PlainCredentials("guest", "guest"),
                    socket_timeout=attempt_timeout,
                    blocked_connection_timeout=attempt_timeout,
                    stack_timeout=attempt_timeout,
                    heartbeat=0,
                )

                try:
                    connection = pika.BlockingConnection(parameters)
                    try:
                        channel = connection.channel()
                        try:
                            for queue_name in self._omq_queue_names(extra_args):
                                channel.queue_declare(
                                    queue=queue_name,
                                    durable=True,
                                    exclusive=False,
                                    auto_delete=False,
                                )
                                channel.queue_purge(queue=queue_name)
                        finally:
                            try:
                                channel.close()
                            except Exception:
                                pass
                    finally:
                        connection.close()
                    return None
                except Exception as e:
                    last_error = e
                    sleep_for = min(0.5, max(0.0, deadline - time.monotonic()))
                    if sleep_for > 0:
                        time.sleep(sleep_for)
        except Exception as e:
            return f"failed to prepare omq queues: {e}"
        if last_error is not None:
            return f"failed to prepare omq queues: {last_error}"
        return "failed to prepare omq queues: timed out waiting for broker readiness"

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

register_benchmark("mq_bench", MessageQueueBenchRunner)
