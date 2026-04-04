"""
Test Runner Core Module

Provides the main test orchestration logic.
"""

import json
import logging
import shutil
import socket
import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Set, Tuple

from sut import SystemUnderTest, create_sut
from benchmarks import BenchmarkRunner, BenchmarkResult, BenchmarkStatus, create_benchmark
from feedback import FeedbackData, TextFeedbackFormatter, anonymize_feedback_data

logger = logging.getLogger(__name__)


@dataclass
class TierResult:
    """Result from a single benchmark tier."""
    tier: str
    status: str
    started_at: str = ""
    finished_at: str = ""
    output_dir: Optional[str] = None
    suites: Dict[str, str] = field(default_factory=dict)
    reason: Optional[str] = None
    detail: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TestCycleResult:
    """Result from a complete test cycle."""
    __test__ = False

    run_id: str
    test_index: int
    cycle_id: str
    overall_status: str
    tiers: List[TierResult] = field(default_factory=list)
    score: float = 0.0
    passed_count: int = 0
    total_count: int = 0
    test_start: str = ""
    test_end: str = ""
    error: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "run_id": self.run_id,
            "test_index": self.test_index,
            "cycle_id": self.cycle_id,
            "overall_status": self.overall_status,
            "tiers": [
                {
                    "tier": t.tier,
                    "status": t.status,
                    "started_at": t.started_at,
                    "finished_at": t.finished_at,
                    "output_dir": t.output_dir,
                    "suites": t.suites,
                    "reason": t.reason,
                    "detail": t.detail,
                    "error": t.error,
                }
                for t in self.tiers
            ],
            "score": self.score,
            "passed_count": self.passed_count,
            "total_count": self.total_count,
            "test_start": self.test_start,
            "test_end": self.test_end,
            "error": self.error,
            **self.meta,
        }


class TestOrchestrator:
    """
    Generic test orchestrator for running benchmarks against SUTs.

    Handles:
    - Copying SUT code to isolated test directories
    - Starting and stopping SUTs
    - Running benchmark suites
    - Collecting and reporting results
    """
    __test__ = False

    # Default test tiers
    DEFAULT_TIERS = ["L0", "L1", "L2", "L3"]
    LADDER_TIER_MODE = "ladder"
    FULL_TIER_MODE = "full"

    def __init__(
        self,
        sut: SystemUnderTest,
        benchmarks: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize test orchestrator.

        Args:
            sut: System Under Test instance
            benchmarks: List of benchmark names to run
            config: Configuration dictionary
        """
        self.sut = sut
        self.benchmark_names = benchmarks or []
        self.config = config or {}

        # Directories
        self.work_dir = Path(self.config.get("work_dir", ".")).resolve()
        self.test_base_dir = self._resolve_dir(
            self.config.get("test_base_dir") or "test_instances",
            base_dir=self.work_dir,
        )
        self.output_base_dir = self._resolve_dir(
            self.config.get("output_base_dir") or "output",
            base_dir=self.work_dir,
        )

        # Test tiers
        self.tiers = self.config.get("tiers", self.DEFAULT_TIERS)

        # Tier mode controls both execution and feedback scope.
        configured_tier_mode = self.config.get("tier_mode")
        if configured_tier_mode is None:
            configured_tier_mode = (
                self.FULL_TIER_MODE
                if bool(self.config.get("run_all_tiers", True))
                else self.LADDER_TIER_MODE
            )
        self.tier_mode = self._normalize_tier_mode(configured_tier_mode)
        self.run_all_tiers = self.tier_mode == self.FULL_TIER_MODE

        # Port allocation
        self._port_lock = threading.Lock()
        self._allocated_ports: Set[int] = set()

        # Running processes tracking
        self._lock = threading.Lock()
        self._running_tests: Dict[str, Dict[str, Any]] = {}
        self._brief_lock = threading.Lock()

    @classmethod
    def _normalize_tier_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if normalized == cls.LADDER_TIER_MODE:
            return cls.LADDER_TIER_MODE
        return cls.FULL_TIER_MODE

    @staticmethod
    def _is_failure_status(status: str) -> bool:
        return status in ("Wrong Answer", "FAIL", "Time Limit Exceeded", "Runtime Error", "Run Time Error")

    def _resolve_dir(self, value: Any, base_dir: Path) -> Path:
        path = Path(str(value)).expanduser()
        if not path.is_absolute():
            path = base_dir / path
        return path.resolve()

    def run_cycle(
        self,
        run_id: str,
        test_index: int,
        benchmark_timeout_sec: int = 600,
        snapshot_commit: Optional[str] = None,
        snapshot_time: Optional[str] = None,
    ) -> TestCycleResult:
        """
        Run a complete test cycle.

        Args:
            run_id: Run identifier
            test_index: Test cycle index
            benchmark_timeout_sec: Timeout for each benchmark
            snapshot_commit: Git commit to test (optional)

        Returns:
            TestCycleResult
        """
        cycle_id = f"{run_id}__{test_index}"
        test_start = datetime.now().isoformat(timespec="seconds")
        if snapshot_time is None:
            snapshot_time = test_start

        logger.info(f"\n{'=' * 60}")
        logger.info(f"Starting test cycle: {cycle_id}")
        logger.info(f"{'=' * 60}\n")

        # Setup output directory
        output_root = self.output_base_dir / run_id / f"output_{test_index}"
        output_root.mkdir(parents=True, exist_ok=True)
        finalized = False

        def finalize_result() -> TestCycleResult:
            nonlocal finalized
            if finalized:
                return result
            result.test_end = datetime.now().isoformat(timespec="seconds")
            self._write_meta(output_root, result)
            self._write_feedback(result, output_root)
            logger.info(f"Test cycle {cycle_id} completed: {result.overall_status}\n")
            finalized = True
            return result

        # Initialize result
        result = TestCycleResult(
            run_id=run_id,
            test_index=test_index,
            cycle_id=cycle_id,
            overall_status="Pending",
            test_start=test_start,
            meta={
                "sut_type": self.sut.name,
                "source_dir": str(self.sut.work_dir),
                "output_root": str(output_root),
                "agent": self.config.get("agent", ""),
                "agent_type": self.config.get("agent_type", ""),
                "agent_model": self.config.get("agent_model", ""),
                "tier_mode": self.tier_mode,
                "run_all_tiers": self.run_all_tiers,
                "snapshot_time": snapshot_time,
            },
        )

        # Pre-calculate planned total so early-exit paths report correct denominator
        planned_total = self._planned_total_cases()

        # Check if SUT has implementation files
        if not self.sut.has_implementation_files():
            result.overall_status = "Run Time Error"
            result.error = "No implementation files found"
            result.total_count = planned_total
            return finalize_result()

        # Copy SUT to test directory
        test_dir = self._copy_sut(run_id, test_index, snapshot_commit)
        if not test_dir:
            result.overall_status = "Run Time Error"
            result.error = "Failed to copy SUT"
            result.total_count = planned_total
            return finalize_result()

        result.meta["test_dir"] = str(test_dir)

        # Allocate port and start SUT
        host = self.config.get("host", "127.0.0.1")
        port = self._reserve_port(host)
        result.meta["db_host"] = host
        result.meta["db_port"] = port

        # Create a test-specific SUT instance
        test_sut = create_sut(self.sut.name, test_dir, self.sut.config)
        sut_process = test_sut.start(host=host, port=port)

        if not sut_process:
            result.overall_status = "Run Time Error"
            result.error = "Failed to start SUT"
            result.total_count = planned_total
            self._release_port(port)
            return finalize_result()

        # Track running test
        with self._lock:
            self._running_tests[cycle_id] = {
                "sut": test_sut,
                "process": sut_process,
                "host": host,
                "port": port,
            }

        try:
            # Wait for SUT to be ready
            if not test_sut.check_ready(host, port, timeout=30):
                result.overall_status = "Time Limit Exceeded"
                ready_detail = getattr(test_sut, "last_ready_error", None)
                if ready_detail:
                    result.error = f"SUT did not become ready: {ready_detail}"
                else:
                    result.error = "SUT did not become ready"
                result.total_count = planned_total
                return finalize_result()

            # Run benchmark tiers
            tier_results = []
            tier_failed = False

            for tier in self.tiers:
                if tier_failed and not self.run_all_tiers:
                    # Skip remaining tiers after failure
                    tier_results.append(TierResult(
                        tier=tier,
                        status="SKIPPED",
                        reason=f"previous_tier_failed",
                    ))
                    continue

                tier_result = self._run_tier(
                    tier,
                    host,
                    port,
                    output_root / tier,
                    benchmark_timeout_sec,
                )
                tier_results.append(tier_result)

                if self._is_failure_status(tier_result.status):
                    tier_failed = True

            result.tiers = tier_results

            # Calculate overall status and score
            result.overall_status = self._calculate_overall_status(tier_results)
            result.score, result.passed_count, result.total_count = \
                self._calculate_score(tier_results)

        finally:
            # Cleanup
            logger.info(f"Stopping SUT for {cycle_id}")
            test_sut.stop()

            with self._lock:
                self._running_tests.pop(cycle_id, None)

            self._release_port(port)

        return finalize_result()

    def _run_tier(
        self,
        tier: str,
        host: str,
        port: int,
        output_dir: Path,
        timeout_sec: int,
    ) -> TierResult:
        """Run benchmarks for a single tier."""
        output_dir.mkdir(parents=True, exist_ok=True)
        tier_start = datetime.now().isoformat(timespec="seconds")

        logger.info(f"Running tier: {tier}")

        tier_timeout_multipliers = self.config.get("tier_timeout_multipliers") or {}
        try:
            multiplier = float(tier_timeout_multipliers.get(tier, 1.0))
        except Exception:
            multiplier = 1.0
        if multiplier <= 0:
            multiplier = 1.0
        tier_timeout_sec = max(1, int(timeout_sec * multiplier))

        tier_result = TierResult(
            tier=tier,
            status="Pending",
            started_at=tier_start,
            output_dir=str(output_dir),
        )

        suite_results = {}
        has_failure = False
        has_runtime_error = False
        has_timeout = False

        for bench_name in self.benchmark_names:
            logger.info(f"Running {tier}/{bench_name}...")

            try:
                tier_configs = self.config.get("tier_configs", {})
                bench_cfg = None
                if isinstance(tier_configs, dict):
                    tier_cfg = tier_configs.get(tier, {})
                    if isinstance(tier_cfg, dict):
                        bench_cfg = tier_cfg.get(bench_name)

                if not isinstance(bench_cfg, dict):
                    bench_cfg = self.config.get(bench_name, {})

                benchmark = create_benchmark(bench_name, bench_cfg)
                bench_timeout = tier_timeout_sec
                if isinstance(bench_cfg, dict) and "timeout_sec" in bench_cfg:
                    try:
                        bench_timeout = max(1, int(bench_cfg.get("timeout_sec")))
                    except Exception:
                        bench_timeout = tier_timeout_sec
                run_kwargs: Dict[str, Any] = {"tier": tier}

                result = benchmark.run(
                    sut_host=host,
                    sut_port=port,
                    output_dir=output_dir / bench_name,
                    timeout_sec=bench_timeout,
                    **run_kwargs,
                )

                if result.workload_results:
                    # Expand per-workload results into suite entries
                    for wl_name, wl_status in result.workload_results.items():
                        suite_results[f"{bench_name}:{wl_name}"] = wl_status
                        if wl_status in ("PASS", "SKIP"):
                            continue
                        if wl_status in ("RUNTIME_ERROR", "ERROR"):
                            has_runtime_error = True
                            continue
                        if wl_status in ("TIMEOUT", "TIME_LIMIT_EXCEEDED"):
                            has_timeout = True
                            continue
                        if wl_status not in ("PASS", "SKIP"):
                            has_failure = True
                    if result.error and not tier_result.error:
                        tier_result.error = result.error
                    if result.status == BenchmarkStatus.RUNTIME_ERROR:
                        has_runtime_error = True
                    elif result.status == BenchmarkStatus.TIME_LIMIT_EXCEEDED:
                        has_timeout = True
                elif result.status == BenchmarkStatus.ACCEPTED:
                    suite_results[bench_name] = "PASS"
                elif result.status == BenchmarkStatus.SKIPPED:
                    suite_results[bench_name] = "SKIP"
                elif result.status == BenchmarkStatus.TIME_LIMIT_EXCEEDED:
                    suite_results[bench_name] = "TIMEOUT"
                    has_timeout = True
                    if result.error and not tier_result.error:
                        tier_result.error = result.error
                elif result.status == BenchmarkStatus.RUNTIME_ERROR:
                    suite_results[bench_name] = "RUNTIME_ERROR"
                    has_runtime_error = True
                    if result.error and not tier_result.error:
                        tier_result.error = result.error
                else:
                    suite_results[bench_name] = "FAIL"
                    has_failure = True
                    if result.error:
                        tier_result.error = result.error

            except Exception as e:
                logger.error(f"Benchmark {bench_name} failed: {e}")
                suite_results[bench_name] = "ERROR"
                has_failure = True
                tier_result.error = str(e)

        tier_result.suites = suite_results
        tier_result.finished_at = datetime.now().isoformat(timespec="seconds")

        if suite_results and all(v == "SKIP" for v in suite_results.values()):
            tier_result.status = "Skipped"
        elif has_timeout:
            tier_result.status = "Time Limit Exceeded"
        elif has_runtime_error:
            tier_result.status = "Runtime Error"
        elif has_failure:
            tier_result.status = "Wrong Answer"
        else:
            tier_result.status = "Accepted"

        return tier_result

    def _copy_sut(
        self,
        run_id: str,
        test_index: int,
        snapshot_commit: Optional[str] = None
    ) -> Optional[Path]:
        """Copy SUT to test directory."""
        parent_dir = self.test_base_dir / run_id
        test_dir = parent_dir / f"test_instance_{test_index}"

        try:
            parent_dir.mkdir(parents=True, exist_ok=True)

            if test_dir.exists():
                logger.warning(f"Test directory exists, removing: {test_dir}")
                shutil.rmtree(test_dir)

            # Try git archive if snapshot_commit provided
            if snapshot_commit and self._is_git_repo(self.sut.work_dir):
                logger.info(f"Exporting git snapshot: {snapshot_commit[:12]}")
                if self._export_git_snapshot(self.sut.work_dir, snapshot_commit, test_dir):
                    return test_dir
                logger.warning("Git snapshot export failed, falling back to copy")

            # Direct copy
            logger.info(f"Copying SUT from {self.sut.work_dir} to {test_dir}")
            shutil.copytree(self.sut.work_dir, test_dir)
            return test_dir

        except Exception as e:
            logger.error(f"Failed to copy SUT: {e}")
            return None

    def _is_git_repo(self, path: Path) -> bool:
        """Check if path is a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=str(path),
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _export_git_snapshot(
        self,
        repo_dir: Path,
        commit: str,
        dest_dir: Path
    ) -> bool:
        """Export git snapshot to directory."""
        git_proc = None
        tar_proc = None
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            git_proc = subprocess.Popen(
                ["git", "archive", "--format=tar", commit],
                cwd=str(repo_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            tar_proc = subprocess.Popen(
                ["tar", "-xf", "-", "-C", str(dest_dir)],
                stdin=git_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Allow git_proc to receive SIGPIPE if tar_proc exits
            if git_proc.stdout:
                git_proc.stdout.close()
            tar_proc.communicate(timeout=300)
            git_proc.communicate(timeout=300)
            return git_proc.returncode == 0 and tar_proc.returncode == 0
        except subprocess.TimeoutExpired:
            logger.warning("Git snapshot export timed out")
            return False
        except Exception as e:
            logger.warning(f"Git snapshot export failed: {e}")
            return False
        finally:
            # Ensure processes are cleaned up
            for proc in (git_proc, tar_proc):
                if proc is not None:
                    try:
                        if proc.poll() is None:
                            proc.kill()
                        proc.wait(timeout=5)
                    except Exception:
                        pass

    def _reserve_port(self, host: str, max_attempts: int = 100) -> int:
        """Reserve a free port."""
        with self._port_lock:
            for _ in range(max_attempts):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((host, 0))
                    port = s.getsockname()[1]
                if port not in self._allocated_ports:
                    self._allocated_ports.add(port)
                    logger.debug(f"Reserved port {port}")
                    return port
            raise RuntimeError(f"Failed to allocate port after {max_attempts} attempts")

    def _release_port(self, port: int) -> None:
        """Release a reserved port."""
        with self._port_lock:
            self._allocated_ports.discard(port)
            logger.debug(f"Released port {port}")

    def _calculate_overall_status(self, tiers: List[TierResult]) -> str:
        """Calculate overall status from tier results."""
        for tier in tiers:
            # Support both old and new status value names
            if tier.status in ("Time Limit Exceeded", "TIME_LIMIT_EXCEEDED"):
                return "Time Limit Exceeded"
            if tier.status in ("Run Time Error", "Runtime Error"):
                return "Runtime Error"
            if tier.status in ("Wrong Answer", "FAIL"):
                return "Wrong Answer"
        if not tiers:
            return "Run Time Error"
        return "Accepted"

    def _calculate_score(
        self,
        tiers: List[TierResult]
    ) -> Tuple[float, int, int]:
        """Calculate score from tier results.

        Each (tier, workload) pair is scored independently — workloads
        with the same name in different tiers are treated as distinct
        test points because they run under different configurations
        (e.g. sysbench with different table sizes / thread counts).
        """
        passed = 0
        for tier in tiers:
            for status in tier.suites.values():
                if status == "PASS":
                    passed += 1

        total = self._planned_total_cases()
        score = (passed / total * 100) if total > 0 else 0.0
        return score, passed, total

    @staticmethod
    def _status_rank(status: str) -> int:
        normalized = str(status or "").strip().upper()
        if normalized == "PASS":
            return 0
        if normalized in {"FAIL", "WRONG_ANSWER"}:
            return 1
        if normalized in {"TIMEOUT", "TIME_LIMIT_EXCEEDED"}:
            return 2
        if normalized in {"RUNTIME_ERROR", "ERROR"}:
            return 3
        return 1

    def _planned_total_cases(self) -> int:
        """
        Calculate total planned benchmark points from config.

        A point is counted for each workload within each (tier, benchmark)
        where the benchmark is enabled. Benchmarks that report workload_results
        contribute multiple points based on their planned_workload_count().
        """
        tier_configs = self.config.get("tier_configs", {})
        if not isinstance(tier_configs, dict):
            tier_configs = {}

        total = 0
        planned_keys_seen: Set[Tuple[str, str, str]] = set()
        for tier in self.tiers:
            bench_cfgs = tier_configs.get(tier, {})
            if not isinstance(bench_cfgs, dict):
                bench_cfgs = {}

            for bench_name in self.benchmark_names:
                bench_cfg = bench_cfgs.get(bench_name, {})
                if not isinstance(bench_cfg, dict):
                    bench_cfg = {}
                if bench_cfg.get("enabled", True) is False:
                    continue

                try:
                    benchmark = create_benchmark(bench_name, bench_cfg)
                    workload_ids = benchmark.planned_workload_ids(tier=tier)
                    if workload_ids:
                        for workload_id in workload_ids:
                            workload_key = str(workload_id).strip()
                            if not workload_key:
                                continue
                            key = (str(tier), str(bench_name), workload_key)
                            if key in planned_keys_seen:
                                continue
                            planned_keys_seen.add(key)
                            total += 1
                        continue
                    wl_count = benchmark.planned_workload_count(tier=tier)
                    total += max(1, wl_count)
                except Exception:
                    total += 1

        logger.debug(
            "Planned total benchmark points: %d (tiers=%s, benchmarks=%s)",
            total, self.tiers, self.benchmark_names,
        )
        return total

    def _write_meta(self, output_root: Path, result: TestCycleResult) -> None:
        """Write meta.json file."""
        try:
            meta_path = output_root / "meta.json"
            meta_path.write_text(
                json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception as e:
            logger.warning(f"Failed to write meta.json: {e}")

    def _write_feedback(self, result: TestCycleResult, output_root: Path) -> None:
        """Write feedback file."""
        try:
            feedback_tiers = self._select_feedback_tiers(result.tiers)

            # Extract error message from tiers if not already set at top level
            error_msg = result.error
            if not error_msg and result.overall_status in (
                "Wrong Answer", "Runtime Error", "Time Limit Exceeded"
            ):
                for t in feedback_tiers:
                    if t.error:
                        error_msg = t.error
                        break

            # Create FeedbackData
            data = FeedbackData(
                version_id=result.cycle_id,
                run_id=result.run_id,
                test_index=result.test_index,
                agent=result.meta.get("agent", ""),
                snapshot_time=result.meta.get("snapshot_time", ""),
                test_start=result.test_start,
                test_end=result.test_end,
                overall_status=result.overall_status,
                tiers=[
                    {
                        "tier": t.tier,
                        "status": t.status,
                        "suites": t.suites,
                        "reason": t.reason,
                        "detail": t.detail,
                        "error": t.error,
                    }
                    for t in feedback_tiers
                ],
                score=result.score,
                passed_count=result.passed_count,
                total_count=result.total_count,
                error_message=error_msg,
            )

            # Write to output directory (internal, with real names)
            formatter = TextFeedbackFormatter()
            brief_path = output_root / f"last_brief_{result.cycle_id}.txt"
            formatter.write(brief_path, data)

            # Anonymize tool/client names for the agent-facing brief so that
            # agents cannot reverse-engineer which test clients are used.
            anon_tiers, anon_error = anonymize_feedback_data(
                data.tiers, data.error_message
            )
            anon_data = FeedbackData(
                version_id=data.version_id,
                run_id=data.run_id,
                test_index=data.test_index,
                agent=data.agent,
                snapshot_time=data.snapshot_time,
                test_start=data.test_start,
                test_end=data.test_end,
                overall_status=data.overall_status,
                tiers=anon_tiers,
                score=data.score,
                passed_count=data.passed_count,
                total_count=data.total_count,
                error_message=anon_error,
            )

            # Write anonymized brief to SUT directory (what agents read)
            with self._brief_lock:
                if hasattr(self.sut, "get_next_brief_summary_file"):
                    sut_brief_path = self.sut.get_next_brief_summary_file()
                else:
                    sut_brief_path = self.sut.get_brief_summary_file()
                formatter.write(sut_brief_path, anon_data)

        except Exception as e:
            logger.warning(f"Failed to write feedback: {e}")

    def _select_feedback_tiers(self, tiers: List[TierResult]) -> List[TierResult]:
        if self.tier_mode != self.LADDER_TIER_MODE:
            return tiers

        for tier in tiers:
            if self._is_failure_status(tier.status):
                return [tier]
        return tiers

    def cleanup_all(self) -> None:
        """Cleanup all running tests."""
        with self._lock:
            tests_copy = list(self._running_tests.items())

        for cycle_id, info in tests_copy:
            sut = info.get("sut")
            if sut:
                logger.info(f"Stopping test {cycle_id}")
                sut.stop()

            with self._lock:
                self._running_tests.pop(cycle_id, None)
