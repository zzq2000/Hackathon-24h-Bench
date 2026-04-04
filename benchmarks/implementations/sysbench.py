"""
Sysbench Benchmark Runner Implementation

Runs Sysbench OLTP benchmarks against MySQL-compatible databases.
"""

import json
import hashlib
import logging
import os
import re
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

from ..base import BenchmarkRunner, BenchmarkResult, BenchmarkStatus

logger = logging.getLogger(__name__)


# Sysbench output parsing patterns
_SYSBENCH_PATTERNS = {
    "transactions": re.compile(r"^\s*transactions:\s+(\d+)\s+\(([\d.]+)\s+per sec\.\)", re.M),
    "queries": re.compile(r"^\s*queries:\s+(\d+)\s+\(([\d.]+)\s+per sec\.\)", re.M),
    "events": re.compile(r"^\s*events:\s+(\d+)\s+\(([\d.]+)\s+per sec\.\)", re.M),
    "latency_min": re.compile(r"^\s*min:\s*([\d.]+)", re.M),
    "latency_avg": re.compile(r"^\s*avg:\s*([\d.]+)", re.M),
    "latency_max": re.compile(r"^\s*max:\s*([\d.]+)", re.M),
    "latency_p95": re.compile(r"^\s*95th percentile:\s*([\d.]+)", re.M),
    "total_time": re.compile(r"^\s*total time:\s*([\d.]+)s", re.M),
    "total_events": re.compile(r"^\s*total number of events:\s*(\d+)", re.M),
    "threads": re.compile(r"^Number of threads:\s*(\d+)", re.M),
}


@dataclass
class SysbenchWorkload:
    """Configuration for a single Sysbench workload."""
    name: str = "oltp_read_write"
    tables: int = 8
    table_size: int = 100000
    threads: List[int] = field(default_factory=lambda: [1, 4, 8])
    time_sec: int = 60
    warmup_sec: int = 10
    report_interval_sec: int = 1
    db_name: str = "sbtest"
    extra_args: List[str] = field(default_factory=list)


class SysbenchRunner(BenchmarkRunner):
    """
    Sysbench benchmark runner for MySQL-compatible databases.

    Runs OLTP workloads using Sysbench via Docker container.

    Supported workloads:
    - oltp_read_write
    - oltp_read_only
    - oltp_write_only
    - oltp_point_select
    - oltp_update_index
    - oltp_update_non_index
    - oltp_insert
    - oltp_delete
    """

    name = "sysbench"
    description = "Sysbench OLTP benchmark for MySQL-compatible databases"
    supported_suts = ["database"]

    SUPPORTED_WORKLOAD_NAMES = [
        "oltp_read_write",
        "oltp_read_only",
        "oltp_write_only",
        "oltp_point_select",
        "oltp_update_index",
        "oltp_update_non_index",
        "oltp_insert",
        "oltp_delete",
    ]

    # Default Docker configuration
    DEFAULT_IMAGE = "severalnines/sysbench:latest"
    DEFAULT_NETWORK_MODE = "host"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.docker_image = self.config.get("docker_image", self.DEFAULT_IMAGE)
        self.network_mode = self.config.get("network_mode", self.DEFAULT_NETWORK_MODE)
        self.db_user = self.config.get("db_user", "root")
        self.db_password = self.config.get("db_password", "root")
        self.db_name = self.config.get("db_name", "sbtest")

    def _extract_fatal_line(self, output: str) -> Optional[str]:
        for line in (output or "").splitlines():
            if "FATAL:" in line:
                return line.strip()
        return None

    def _extract_failure_line(self, output: str) -> Optional[str]:
        failure_patterns = ("FATAL:", "FINISHED FAILED", "Error in Virtual User")
        for line in (output or "").splitlines():
            text = line.strip()
            if not text:
                continue
            if any(pattern in text for pattern in failure_patterns):
                return text
        return None

    def _sanitize_db_name(self, value: str) -> str:
        sanitized = re.sub(r"[^a-zA-Z0-9_]+", "_", str(value or ""))
        sanitized = re.sub(r"_+", "_", sanitized).strip("_").lower()
        return sanitized or "sbtest"

    def _derive_scoped_db_name(
        self,
        base_db_name: str,
        tier: Optional[str],
        workload_name: str,
    ) -> str:
        base = self._sanitize_db_name(base_db_name)
        tier_part = self._sanitize_db_name(tier or "") if tier else ""
        wl = self._sanitize_db_name(workload_name)
        parts = [base]
        if tier_part:
            parts.append(tier_part)
        parts.append(wl)
        full = "_".join(parts)
        if len(full) <= 64:
            return full
        digest = hashlib.sha1(full.encode("utf-8")).hexdigest()[:8]
        keep = 64 - (len(digest) + 1)
        return f"{full[:keep]}_{digest}"

    def run(
        self,
        sut_host: str,
        sut_port: int,
        output_dir: Path,
        timeout_sec: int = 600,
        **kwargs
    ) -> BenchmarkResult:
        """
        Run Sysbench benchmark.

        Args:
            sut_host: Database host
            sut_port: Database port
            output_dir: Output directory
            timeout_sec: Timeout in seconds
            **kwargs: workload config, etc.

        Returns:
            BenchmarkResult
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "raw" / "sysbench"
        raw_dir.mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        if self.config.get("enabled") is False:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.SKIPPED,
                details="Sysbench disabled by config",
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )

        workloads = self._get_workloads(kwargs)
        if not workloads:
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error="Invalid sysbench config: no workloads to run",
                output_dir=output_dir,
                elapsed_sec=time.time() - start_time,
            )

        enabled_workloads = self.config.get("enabled_workloads")
        if enabled_workloads is not None:
            if not isinstance(enabled_workloads, list):
                return BenchmarkResult(
                    status=BenchmarkStatus.RUNTIME_ERROR,
                    error="Invalid sysbench config: enabled_workloads must be a list",
                    output_dir=output_dir,
                    elapsed_sec=time.time() - start_time,
                )
            enabled_set = {str(x).strip() for x in enabled_workloads if str(x).strip()}
            if not enabled_set:
                elapsed = time.time() - start_time
                return BenchmarkResult(
                    status=BenchmarkStatus.SKIPPED,
                    details="Sysbench skipped: enabled_workloads is empty",
                    output_dir=output_dir,
                    elapsed_sec=elapsed,
                )
            supported = set(self.SUPPORTED_WORKLOAD_NAMES)
            unknown = sorted(enabled_set - supported)
            if unknown:
                return BenchmarkResult(
                    status=BenchmarkStatus.RUNTIME_ERROR,
                    error=f"Invalid sysbench config: unknown workloads in enabled_workloads: {', '.join(unknown)}",
                    output_dir=output_dir,
                    elapsed_sec=time.time() - start_time,
                )
            workloads = [w for w in workloads if w.name in enabled_set]

        all_metrics: Dict[str, Any] = {}
        workload_detail_list: List[Dict[str, Any]] = []
        failed_workloads: List[str] = []
        first_error: Optional[str] = None
        first_failed_output: Optional[str] = None
        cleanup_enabled = bool(self.config.get("cleanup", False))

        for workload in workloads:
            remaining = timeout_sec - (time.time() - start_time)
            if remaining <= 0:
                elapsed = time.time() - start_time
                return BenchmarkResult(
                    status=BenchmarkStatus.TIME_LIMIT_EXCEEDED,
                    error="Sysbench exceeded benchmark timeout while running workloads",
                    raw_output=first_failed_output or "",
                    output_dir=output_dir,
                    elapsed_sec=elapsed,
                )

            # Normalize and validate thread counts to avoid crashes on misconfiguration (e.g., threads: []).
            normalized_threads, threads_error = self._normalize_thread_counts(workload.threads)
            if threads_error:
                return BenchmarkResult(
                    status=BenchmarkStatus.RUNTIME_ERROR,
                    error=threads_error,
                    output_dir=output_dir,
                    elapsed_sec=time.time() - start_time,
                )
            workload.threads = normalized_threads

            # Ensure database exists
            db_create_ok = self._ensure_database(
                sut_host, sut_port, workload.db_name
            )
            if not db_create_ok:
                return BenchmarkResult(
                    status=BenchmarkStatus.RUNTIME_ERROR,
                    error="Failed to create database",
                    output_dir=output_dir,
                    elapsed_sec=time.time() - start_time,
                )

            logger.info(f"Running Sysbench workload: {workload.name}")

            workload_metrics: Dict[str, Any] = {}
            run_results: List[Dict[str, Any]] = []
            warmup_result: Optional[Dict[str, Any]] = None

            # Prepare phase
            logger.info(f"Running Sysbench prepare for {workload.name}...")
            remaining = timeout_sec - (time.time() - start_time)
            prepare_result = self._run_sysbench_phase(
                "prepare",
                sut_host,
                sut_port,
                workload,
                raw_dir / f"{workload.name}_prepare.log",
                max(1, int(remaining)),
            )

            workload_status = BenchmarkStatus.ACCEPTED
            workload_error = None

            prepare_output = prepare_result.get("output", "") or ""
            prepare_failure = self._extract_failure_line(prepare_output)
            if prepare_result["returncode"] != 0 or prepare_failure:
                workload_status = BenchmarkStatus.WRONG_ANSWER
                prepare_error = (
                    prepare_result.get("error")
                    or prepare_failure
                    or self._extract_fatal_line(prepare_output)
                    or "unknown"
                )
                workload_error = f"Sysbench prepare failed: {prepare_error}"
                failed_workloads.append(workload.name)
                if first_error is None:
                    first_error = workload_error
                    first_failed_output = prepare_output
            else:
                # Warmup phase (if configured) - runs separately to avoid --warmup-time
                # which is not supported in sysbench 1.0.17
                if workload.warmup_sec > 0:
                    logger.info(f"Running Sysbench warmup for {workload.name} ({workload.warmup_sec}s)...")
                    remaining = timeout_sec - (time.time() - start_time)
                    warmup_result = self._run_sysbench_phase(
                        "run",
                        sut_host,
                        sut_port,
                        workload,
                        raw_dir / f"{workload.name}_warmup.log",
                        max(1, min(int(remaining), workload.warmup_sec + 60)),
                        threads=workload.threads[0],
                        run_time_override=workload.warmup_sec,
                    )
                    if warmup_result["returncode"] != 0:
                        warmup_output = warmup_result.get("output", "") or ""
                        warmup_error = (
                            warmup_result.get("error")
                            or self._extract_failure_line(warmup_output)
                            or self._extract_fatal_line(warmup_output)
                        )
                        logger.warning(
                            f"Sysbench warmup failed for {workload.name} (non-fatal): "
                            f"{warmup_error or 'unknown'}"
                        )

                # Run phase for each thread count
                for thread_count in workload.threads:
                    logger.info(f"Running Sysbench {workload.name} with {thread_count} threads...")
                    remaining = timeout_sec - (time.time() - start_time)
                    run_result = self._run_sysbench_phase(
                        "run",
                        sut_host,
                        sut_port,
                        workload,
                        raw_dir / f"{workload.name}_run_t{thread_count}.log",
                        max(1, min(int(remaining), workload.time_sec + 120)),
                        threads=thread_count,
                    )

                    run_results.append(run_result)
                    run_output = run_result.get("output", "") or ""
                    run_failure = self._extract_failure_line(run_output)
                    if run_result["returncode"] == 0 and not run_failure:
                        parsed = self.parse_results(run_result.get("output", ""))
                        if parsed:
                            workload_metrics[f"threads_{thread_count}"] = parsed
                        else:
                            workload_status = BenchmarkStatus.WRONG_ANSWER
                            if workload_error is None:
                                workload_error = "Sysbench run produced no parseable metrics"
                            if workload.name not in failed_workloads:
                                failed_workloads.append(workload.name)
                            if first_error is None:
                                first_error = workload_error
                                first_failed_output = run_output
                    else:
                        workload_status = BenchmarkStatus.WRONG_ANSWER
                        if workload_error is None:
                            workload_error = (
                                run_result.get("error")
                                or run_failure
                                or self._extract_fatal_line(run_output)
                                or "Sysbench run failed"
                            )
                        if workload.name not in failed_workloads:
                            failed_workloads.append(workload.name)
                        if first_error is None:
                            first_error = workload_error
                            first_failed_output = run_result.get("output", "") or ""

                # Cleanup phase (optional)
                if cleanup_enabled:
                    remaining = timeout_sec - (time.time() - start_time)
                    self._run_sysbench_phase(
                        "cleanup",
                        sut_host,
                        sut_port,
                        workload,
                        raw_dir / f"{workload.name}_cleanup.log",
                        max(1, min(int(remaining), 120)),
                    )

            all_metrics[workload.name] = workload_metrics
            workload_detail_list.append({
                "workload": {
                    "name": workload.name,
                    "tables": workload.tables,
                    "table_size": workload.table_size,
                    "threads": workload.threads,
                    "time_sec": workload.time_sec,
                    "warmup_sec": workload.warmup_sec,
                    "report_interval_sec": workload.report_interval_sec,
                    "db_name": workload.db_name,
                    "extra_args": workload.extra_args,
                },
                "prepare": prepare_result,
                "warmup": warmup_result,
                "runs": run_results,
                "metrics": workload_metrics,
                "status": workload_status.name,
                "error": workload_error,
            })

        overall_status = BenchmarkStatus.ACCEPTED if not failed_workloads else BenchmarkStatus.WRONG_ANSWER
        score = self._calculate_score(all_metrics)

        results_file = output_dir / "sysbench_results.json"
        results_file.write_text(
            json.dumps({
                "supported_workloads": list(self.SUPPORTED_WORKLOAD_NAMES),
                "enabled_workloads": (
                    list(enabled_workloads)
                    if isinstance(enabled_workloads, list)
                    else None
                ),
                "cleanup": cleanup_enabled,
                "metrics": all_metrics,
                "workload_results": workload_detail_list,
            }, indent=2),
            encoding="utf-8",
        )

        elapsed = time.time() - start_time
        passed = len(workloads) - len(set(failed_workloads))
        details = f"Sysbench: {passed}/{len(workloads)} workloads passed"
        if failed_workloads:
            details += f" (failed: {', '.join(sorted(set(failed_workloads)))})"

        # Build per-workload results dict for independent scoring
        wl_results: Dict[str, str] = {}
        for wr in workload_detail_list:
            wl_name = wr["workload"]["name"]
            wl_status_str = wr.get("status", "")
            if wl_status_str == "ACCEPTED":
                wl_results[wl_name] = "PASS"
            elif wl_status_str == "SKIPPED":
                wl_results[wl_name] = "SKIP"
            else:
                wl_results[wl_name] = "FAIL"

        return BenchmarkResult(
            status=overall_status,
            score=score,
            metrics=all_metrics,
            details=details,
            error=first_error,
            raw_output=first_failed_output or "",
            output_dir=output_dir,
            elapsed_sec=elapsed,
            workload_results=wl_results,
        )

    def parse_results(self, output: str) -> Dict[str, Any]:
        """
        Parse Sysbench output.

        Args:
            output: Raw Sysbench output

        Returns:
            Parsed metrics dictionary
        """
        metrics = {}
        for key, pattern in _SYSBENCH_PATTERNS.items():
            match = pattern.search(output)
            if not match:
                continue

            if len(match.groups()) == 1:
                val = match.group(1)
                metrics[key] = float(val) if "." in val else int(val)
            else:
                # count + rate
                count, rate = match.group(1), match.group(2)
                metrics[key] = {"count": int(count), "per_sec": float(rate)}

        return metrics

    def _get_workloads(self, kwargs: Dict[str, Any]) -> List[SysbenchWorkload]:
        """
        Build workload configs for all supported workloads.

        Tier-level flat config (e.g., tiers.sysbench.L0.threads) takes
        precedence over per-workload config for overridable parameters.
        """
        base_wl_config = kwargs.get("workload")
        if not isinstance(base_wl_config, dict):
            base_wl_config = self.config.get("workload")
        if not isinstance(base_wl_config, dict):
            base_wl_config = {}

        configured_workloads = self.config.get("workloads")
        by_name: Dict[str, Dict[str, Any]] = {}
        if isinstance(configured_workloads, list):
            for item in configured_workloads:
                if not isinstance(item, dict):
                    continue
                name = (item.get("name") or "").strip()
                if name:
                    by_name[name] = item

        tier_override_keys = {
            "tables", "table_size", "threads", "time_sec",
            "warmup_sec", "report_interval_sec", "extra_args",
        }

        def _get(wl_cfg: Dict[str, Any], key: str, default: Any) -> Any:
            if key in tier_override_keys and key in self.config:
                return self.config.get(key, default)
            if key in wl_cfg:
                return wl_cfg.get(key, default)
            if key in base_wl_config:
                return base_wl_config.get(key, default)
            return self.config.get(key, default)

        workloads: List[SysbenchWorkload] = []
        tier = kwargs.get("tier")
        for name in self.SUPPORTED_WORKLOAD_NAMES:
            wl_cfg = by_name.get(name, {})
            base_db_name = _get(wl_cfg, "db_name", self.db_name)
            workloads.append(SysbenchWorkload(
                name=name,
                tables=_get(wl_cfg, "tables", 4),
                table_size=_get(wl_cfg, "table_size", 10000),
                threads=_get(wl_cfg, "threads", [1, 4]),
                time_sec=_get(wl_cfg, "time_sec", 30),
                warmup_sec=_get(wl_cfg, "warmup_sec", 5),
                report_interval_sec=_get(wl_cfg, "report_interval_sec", 1),
                db_name=self._derive_scoped_db_name(base_db_name, str(tier) if tier is not None else None, name),
                extra_args=_get(wl_cfg, "extra_args", []),
            ))

        return workloads

    def _normalize_thread_counts(self, threads: Any) -> Tuple[Optional[List[int]], Optional[str]]:
        if not isinstance(threads, list) or not threads:
            return None, "Invalid sysbench config: workload.threads must contain at least one thread count"
        normalized: List[int] = []
        for thread_count in threads:
            try:
                thread_int = int(thread_count)
            except (TypeError, ValueError):
                return None, f"Invalid sysbench config: thread count must be an integer, got {thread_count!r}"
            if thread_int <= 0:
                return None, f"Invalid sysbench config: thread count must be > 0, got {thread_int}"
            normalized.append(thread_int)
        return normalized, None

    def _ensure_database(self, host: str, port: int, db_name: str) -> bool:
        """Ensure the benchmark database exists."""
        try:
            import pymysql
            db_name_safe = self._sanitize_db_name(db_name)
            conn = pymysql.connect(
                host=host,
                port=port,
                user=self.db_user,
                password=self.db_password,
                connect_timeout=10,
            )
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name_safe}`")
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to create database: {e}")
            return False

    def _run_sysbench_phase(
        self,
        phase: str,
        host: str,
        port: int,
        workload: SysbenchWorkload,
        log_path: Path,
        timeout_sec: int,
        threads: Optional[int] = None,
        run_time_override: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Run a Sysbench phase (prepare/run/cleanup)."""
        # Build Docker command
        cmd = self._build_docker_cmd(phase, host, port, workload, threads, run_time_override)

        logger.debug(f"Sysbench command: {' '.join(cmd)}")

        result = {
            "phase": phase,
            "command": " ".join(cmd),
            "returncode": -1,
            "output": "",
            "error": None,
        }

        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            output_lines = []
            try:
                stdout, _ = proc.communicate(timeout=timeout_sec)
                output_lines.append(stdout or "")
            except subprocess.TimeoutExpired:
                proc.kill()
                stdout, _ = proc.communicate()
                output_lines.append(stdout or "")
                output_lines.append("\n[TIMEOUT]\n")
                result["error"] = "timeout"

            result["output"] = "".join(output_lines)
            result["returncode"] = proc.returncode

            # Write log
            log_path.write_text(result["output"], encoding="utf-8")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Sysbench {phase} failed: {e}")

        return result

    def _build_docker_cmd(
        self,
        phase: str,
        host: str,
        port: int,
        workload: SysbenchWorkload,
        threads: Optional[int] = None,
        run_time_override: Optional[int] = None,
    ) -> List[str]:
        """Build Docker command for Sysbench."""
        cmd = ["docker", "run", "--rm"]

        if self.network_mode == "host":
            cmd += ["--network", "host"]
        else:
            cmd += ["--add-host", "host.docker.internal:host-gateway"]

        cmd.append(self.docker_image)

        # Sysbench arguments
        sysbench_args = [
            "sysbench",
            workload.name,
            f"--mysql-host={self._get_container_host(host)}",
            f"--mysql-port={port}",
            f"--mysql-user={self.db_user}",
            f"--mysql-password={self.db_password}",
            f"--mysql-db={workload.db_name}",
            f"--tables={workload.tables}",
            f"--table-size={workload.table_size}",
        ]

        if phase == "run":
            thread_count = threads if threads is not None else (workload.threads[0] if workload.threads else 1)
            time_sec = run_time_override if run_time_override is not None else workload.time_sec
            sysbench_args += [
                f"--threads={thread_count}",
                f"--time={time_sec}",
                f"--report-interval={workload.report_interval_sec}",
            ]
        else:
            sysbench_args.append(f"--threads={self.config.get('prepare_threads', 4)}")

        if workload.extra_args:
            sysbench_args.extend([str(x) for x in workload.extra_args if str(x).strip()])

        sysbench_args.append(phase)
        cmd.extend(sysbench_args)

        return cmd

    def _get_container_host(self, host: str) -> str:
        """Get host address for container."""
        if self.network_mode == "host":
            return host
        if host in ("127.0.0.1", "localhost"):
            return "host.docker.internal"
        return host

    def _calculate_score_single(self, metrics: Dict[str, Any]) -> float:
        """Calculate score from a single workload's metrics (TPS based)."""
        total_tps = 0.0
        count = 0
        for key, data in metrics.items():
            if isinstance(data, dict) and "transactions" in data:
                txn = data["transactions"]
                if isinstance(txn, dict) and "per_sec" in txn:
                    total_tps += txn["per_sec"]
                    count += 1
        return total_tps / count if count > 0 else 0.0

    def _calculate_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate score from metrics across all workloads (TPS based)."""
        if any(str(k).startswith("threads_") for k in metrics.keys()):
            return self._calculate_score_single(metrics)
        scores: List[float] = []
        for _, workload_metrics in metrics.items():
            if isinstance(workload_metrics, dict):
                score = self._calculate_score_single(workload_metrics)
                if score > 0:
                    scores.append(score)
        return sum(scores) / len(scores) if scores else 0.0

    def planned_workload_count(self, **kwargs) -> int:
        """Return the expected number of workload result entries."""
        enabled_workloads = self.config.get("enabled_workloads")
        if isinstance(enabled_workloads, list):
            enabled_set = {str(x).strip() for x in enabled_workloads if str(x).strip()}
            return len([name for name in self.SUPPORTED_WORKLOAD_NAMES if name in enabled_set])
        return len(self.SUPPORTED_WORKLOAD_NAMES)

    def get_default_config(self) -> Dict[str, Any]:
        """Get default Sysbench configuration."""
        return {
            "docker_image": self.DEFAULT_IMAGE,
            "network_mode": self.DEFAULT_NETWORK_MODE,
            "db_user": "root",
            "db_password": "root",
            "db_name": "sbtest",
            "workload": {
                "name": "oltp_read_write",
                "tables": 4,
                "table_size": 10000,
                "threads": [1, 4],
                "time_sec": 30,
            },
        }


# Register the benchmark
from ..registry import register_benchmark
register_benchmark("sysbench", SysbenchRunner)
