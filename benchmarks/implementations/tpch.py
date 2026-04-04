"""
TPC-H Benchmark Runner Implementation

Runs TPC-H (TPROC-H) benchmarks using HammerDB against MySQL-compatible databases.

Supports fine-grained per-query workload reporting:
- schema: Schema creation phase
- data_load: Data loading phase
- q1..q22: Individual TPC-H query results
"""

import json
import hashlib
import logging
import math
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..base import BenchmarkRunner, BenchmarkResult, BenchmarkStatus
from ._validation import find_success_marker_line, missing_success_marker_error

logger = logging.getLogger(__name__)


# TPC-H output parsing patterns
_TPCH_PATTERNS = {
    "query_time": re.compile(r"[Qq]uery (\d+) completed in ([\d.]+) seconds", re.M),
    "total_time": re.compile(r"Completed \d+ query set\(s\) in (\d+) seconds", re.M),
    "geometric_mean": re.compile(r"Geometric mean of query times.*?is ([\d.]+)", re.M),
    "power_size": re.compile(r"Power Size: ([\d.]+)", re.M),
    "throughput_size": re.compile(r"Throughput Size: ([\d.]+)", re.M),
    "qphh": re.compile(r"QphH: ([\d.]+)", re.M),
}

# All 22 TPC-H standard queries
TPCH_ALL_QUERIES = list(range(1, 23))
_TPCH_BUILD_SUCCESS_MARKERS = ("all virtual users complete", "success")


@dataclass
class TPCHConfig:
    """Configuration for TPC-H benchmark."""
    db_name: str = "tpch"
    scale_factor: float = 1.0
    schema_threads: int = 4
    vus: int = 1
    refresh_on: bool = False
    degree_parallel: int = 2
    storage_engine: str = "innodb"
    ssl: bool = False
    enabled_queries: Optional[List[int]] = None


class TPCHRunner(BenchmarkRunner):
    """
    TPC-H (TPROC-H) benchmark runner for MySQL-compatible databases.

    Uses HammerDB Docker container to run standardized OLAP workloads
    with complex analytical queries.

    Supports fine-grained per-query workload reporting. Each of the 22
    TPC-H queries is reported as an independent workload with its own
    pass/fail status and execution time.

    Workloads:
    - schema: Schema creation
    - data_load: Data loading
    - q1..q22: Individual TPC-H queries
    """

    name = "tpch"
    description = "TPC-H (TPROC-H) OLAP benchmark via HammerDB"
    supported_suts = ["database"]

    # Default Docker configuration
    DEFAULT_IMAGE = "tpcorg/hammerdb:v4.9"
    DEFAULT_NETWORK_MODE = "host"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.docker_image = self.config.get("docker_image", self.DEFAULT_IMAGE)
        self.network_mode = self.config.get("network_mode", self.DEFAULT_NETWORK_MODE)
        self.db_user = self.config.get("db_user", "root")
        self.db_password = self.config.get("db_password", "root")

    def _sanitize_db_name(self, value: str) -> str:
        sanitized = re.sub(r"[^a-zA-Z0-9_]+", "_", str(value or ""))
        sanitized = re.sub(r"_+", "_", sanitized).strip("_").lower()
        return sanitized or "tpch"

    def _derive_tier_db_name(self, base_db_name: str, tier: Optional[str]) -> str:
        base = self._sanitize_db_name(base_db_name)
        if not tier:
            return base
        tier_part = self._sanitize_db_name(tier)
        full = f"{base}_{tier_part}"
        if len(full) <= 64:
            return full
        digest = hashlib.sha1(full.encode("utf-8")).hexdigest()[:8]
        keep = 64 - (len(digest) + 1)
        return f"{full[:keep]}_{digest}"

    def _extract_failure_line(self, output: str) -> Optional[str]:
        failure_patterns = (
            "fatal:",
            "finished failed",
            "error in virtual user",
            "mysqlexec/db server:",
            "sql syntax",
        )
        for line in (output or "").splitlines():
            text = line.strip()
            if not text:
                continue
            lowered = text.lower()
            if any(pattern in lowered for pattern in failure_patterns):
                return text
        return None

    def _parse_build_phases(self, build_output: str, build_returncode: int) -> Dict[str, str]:
        """Parse build output to determine schema and data_load status."""
        output_lower = (build_output or "").lower()
        failure_line = self._extract_failure_line(build_output)

        if build_returncode != 0 or failure_line:
            if failure_line:
                fl = failure_line.lower()
                if any(kw in fl for kw in ("create table", "create index", "alter table")):
                    return {"schema": "FAIL", "data_load": "SKIP"}

            if any(p in output_lower for p in ("loading lineitem", "loading orders", "loading customer", "loading nation")):
                return {"schema": "PASS", "data_load": "FAIL"}

            # No keyword matched — log for observability
            logger.warning(
                "TPC-H build phase could not be determined; returncode=%d, failure_line=%r",
                build_returncode, failure_line,
            )
            return {"schema": "FAIL", "data_load": "FAIL"}

        # Build succeeded overall only when it also emits positive completion evidence.
        if not find_success_marker_line(build_output, _TPCH_BUILD_SUCCESS_MARKERS):
            logger.warning(
                "TPC-H build returned 0 but output lacks success markers (returncode=%d)",
                build_returncode,
            )
            return {"schema": "FAIL", "data_load": "FAIL"}
        return {"schema": "PASS", "data_load": "PASS"}

    def _find_attempted_queries(self, run_output: str, enabled_queries: List[int]) -> set:
        """Determine which queries were attempted based on serial execution model.

        HammerDB runs queries serially. Any enabled query up to the highest
        mentioned query number is considered "attempted".
        """
        mentioned = set()
        for m in re.finditer(r"[Qq]uery\s+(\d+)", run_output or ""):
            mentioned.add(int(m.group(1)))

        if not mentioned:
            return set()

        max_mentioned = max(mentioned)
        # All enabled queries up to (and including) the highest mentioned are attempted
        return {q for q in enabled_queries if q <= max_mentioned}

    def run(
        self,
        sut_host: str,
        sut_port: int,
        output_dir: Path,
        timeout_sec: int = 3600,
        **kwargs
    ) -> BenchmarkResult:
        """
        Run TPC-H benchmark with per-query workload reporting.

        Execution phases:
        1. Build: Schema creation + data loading (one-time)
        2. Run: Execute all 22 TPC-H queries
        3. Report per-query pass/fail based on completion
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "raw" / "tpch"
        raw_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir = output_dir / "scripts" / "tpch"
        scripts_dir.mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        if self.config.get("enabled") is False:
            return BenchmarkResult(
                status=BenchmarkStatus.SKIPPED,
                details="TPC-H disabled by config",
                output_dir=output_dir,
                elapsed_sec=time.time() - start_time,
            )

        # Get TPC-H configuration
        tpch_config = self._get_config(kwargs)
        enabled_queries = tpch_config.enabled_queries or list(TPCH_ALL_QUERIES)

        workload_results: Dict[str, str] = {}
        first_error: Optional[str] = None

        # Ensure database exists
        db_create_ok = self._ensure_database(sut_host, sut_port, tpch_config.db_name)
        if not db_create_ok:
            workload_results["schema"] = "ERROR"
            workload_results["data_load"] = "ERROR"
            for q in enabled_queries:
                workload_results[f"q{q}"] = "ERROR"
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error="Failed to create database",
                output_dir=output_dir,
                elapsed_sec=time.time() - start_time,
                workload_results=workload_results,
            )

        # ── Phase 1: Build schema ──
        build_script = self._generate_build_script(sut_host, sut_port, tpch_config)
        build_script_path = scripts_dir / "tpch_build.tcl"
        build_script_path.write_text(build_script, encoding="utf-8")

        logger.info("Running TPC-H schema build...")
        remaining = timeout_sec - (time.time() - start_time)
        build_result = self._run_hammerdb(
            build_script_path,
            raw_dir / "tpch_build.log",
            max(1, int(remaining // 2)),
        )

        build_output = build_result.get("output", "") or ""
        build_phases = self._parse_build_phases(build_output, build_result["returncode"])

        workload_results["schema"] = build_phases["schema"]
        workload_results["data_load"] = build_phases["data_load"]

        build_failed = (build_phases["schema"] == "FAIL" or build_phases["data_load"] == "FAIL")
        if build_failed:
            first_error = (
                "TPC-H build failed: "
                f"{self._extract_failure_line(build_output) or build_result.get('error') or missing_success_marker_error('TPC-H build', _TPCH_BUILD_SUCCESS_MARKERS)}"
            )
            for q in enabled_queries:
                workload_results[f"q{q}"] = "SKIP"

            self._write_results_file(output_dir, tpch_config, enabled_queries,
                                     {}, build_result, None, workload_results)
            return self._make_result(
                workload_results, {}, tpch_config, first_error, build_output,
                output_dir, start_time,
            )

        # ── Phase 2: Run queries ──
        run_script = self._generate_run_script(sut_host, sut_port, tpch_config)
        run_script_path = scripts_dir / "tpch_run.tcl"
        run_script_path.write_text(run_script, encoding="utf-8")

        logger.info("Running TPC-H queries...")
        remaining = timeout_sec - (time.time() - start_time)
        run_result = self._run_hammerdb(
            run_script_path,
            raw_dir / "tpch_run.log",
            max(1, int(remaining)),
        )

        run_output = run_result.get("output", "") or ""
        run_failure = self._extract_failure_line(run_output)
        metrics = self.parse_results(run_output)
        query_times = metrics.get("query_times", {})

        run_failed = (run_result["returncode"] != 0 or run_failure)
        if run_failed:
            # Run failed overall, but some queries may have completed
            if not first_error:
                first_error = run_failure or run_result.get("error") or "TPC-H run failed"

        # Determine per-query pass/fail/skip
        attempted = self._find_attempted_queries(run_output, enabled_queries)
        run_level_failure_marked = False
        for q in enabled_queries:
            q_key = f"q{q}"
            if q_key in query_times:
                workload_results[q_key] = "PASS"
            elif q in attempted:
                workload_results[q_key] = "FAIL"
                run_level_failure_marked = True
                if not first_error:
                    first_error = f"TPC-H query {q} did not complete"
            else:
                if run_failed:
                    workload_results[q_key] = "FAIL"
                    run_level_failure_marked = True
                    if not first_error:
                        first_error = f"TPC-H query {q} was not reached before run failure"
                else:
                    workload_results[q_key] = "FAIL"
                    run_level_failure_marked = True
                    if not first_error:
                        first_error = f"TPC-H query {q} was not reached despite successful run"

        # If HammerDB reports a run-level failure after all queries appear complete,
        # force at least one workload to fail so overall status is not ACCEPTED.
        if run_failed and not run_level_failure_marked and enabled_queries:
            last_query_key = f"q{enabled_queries[-1]}"
            workload_results[last_query_key] = "FAIL"
            if not first_error:
                first_error = run_failure or run_result.get("error") or "TPC-H run failed"

        self._write_results_file(output_dir, tpch_config, enabled_queries,
                                 metrics, build_result, run_result, workload_results)

        return self._make_result(
            workload_results, metrics, tpch_config, first_error,
            run_output if run_failure else "",
            output_dir, start_time,
        )

    def _make_result(
        self,
        workload_results: Dict[str, str],
        metrics: Dict[str, Any],
        config: TPCHConfig,
        first_error: Optional[str],
        raw_output: str,
        output_dir: Path,
        start_time: float,
    ) -> BenchmarkResult:
        """Build the final BenchmarkResult from workload results."""
        elapsed = time.time() - start_time

        # Determine overall status
        statuses = set(workload_results.values())
        if not statuses or statuses <= {"PASS", "SKIP"}:
            overall = BenchmarkStatus.ACCEPTED
        else:
            overall = BenchmarkStatus.WRONG_ANSWER

        # Calculate score
        if metrics.get("geometric_mean"):
            score = 1000.0 / metrics["geometric_mean"]
        elif metrics.get("total_time"):
            score = 1000.0 / metrics["total_time"]
        else:
            score = 0.0

        # Build details string
        pass_count = sum(1 for s in workload_results.values() if s == "PASS")
        total = len(workload_results)
        failed = [k for k, v in workload_results.items() if v not in ("PASS", "SKIP")]
        details = f"TPC-H SF={config.scale_factor}: {pass_count}/{total} workloads passed"
        if failed:
            details += f" (failed: {', '.join(sorted(failed))})"

        return BenchmarkResult(
            status=overall,
            score=score,
            metrics=metrics,
            details=details,
            error=first_error,
            raw_output=raw_output if overall != BenchmarkStatus.ACCEPTED else "",
            output_dir=output_dir,
            elapsed_sec=elapsed,
            workload_results=workload_results,
        )

    def _write_results_file(
        self,
        output_dir: Path,
        config: TPCHConfig,
        enabled_queries: List[int],
        metrics: Dict[str, Any],
        build_result: Dict[str, Any],
        run_result: Optional[Dict[str, Any]],
        workload_results: Dict[str, str],
    ) -> None:
        """Write tpch_results.json."""
        try:
            results_file = output_dir / "tpch_results.json"
            results_file.write_text(
                json.dumps({
                    "config": {
                        "scale_factor": config.scale_factor,
                        "vus": config.vus,
                        "enabled_queries": enabled_queries,
                    },
                    "metrics": metrics,
                    "workload_results": workload_results,
                    "build": build_result,
                    "run": run_result,
                }, indent=2, default=str),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning(f"Failed to write tpch_results.json: {e}")

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse TPC-H output."""
        metrics = {}

        # Parse individual query times
        query_times = {}
        for match in re.finditer(r"[Qq]uery (\d+) completed in ([\d.]+) seconds", output):
            query_num = int(match.group(1))
            query_time = float(match.group(2))
            query_times[f"q{query_num}"] = query_time
        if query_times:
            metrics["query_times"] = query_times

        # Parse summary metrics
        for key, pattern in _TPCH_PATTERNS.items():
            if key == "query_time":
                continue
            match = pattern.search(output)
            if match:
                metrics[key] = float(match.group(1))

        # Calculate geometric mean if not present
        if query_times and "geometric_mean" not in metrics:
            values = list(query_times.values())
            if values and all(v > 0 for v in values):
                log_sum = sum(math.log(v) for v in values)
                metrics["geometric_mean"] = math.exp(log_sum / len(values))

        return metrics

    def planned_workload_count(self, **kwargs) -> int:
        """Return the expected number of workload result entries."""
        tpch_config = self._get_config(kwargs)
        enabled_queries = tpch_config.enabled_queries or list(TPCH_ALL_QUERIES)
        return 2 + len(enabled_queries)  # schema + data_load + each query

    def _get_config(self, kwargs: Dict[str, Any]) -> TPCHConfig:
        """Get TPC-H configuration."""
        tpch = kwargs.get("tpch")
        if not isinstance(tpch, dict):
            tpch = self.config.get("tpch")
        if not isinstance(tpch, dict):
            tpch = {}

        def _get(key: str, default: Any) -> Any:
            if key in tpch:
                return tpch.get(key, default)
            return self.config.get(key, default)

        enabled_queries_raw = _get("enabled_queries", None)
        enabled_queries = None
        if enabled_queries_raw is not None:
            if isinstance(enabled_queries_raw, list):
                enabled_queries = []
                for q in enabled_queries_raw:
                    try:
                        qi = int(q)
                        if 1 <= qi <= 22:
                            enabled_queries.append(qi)
                    except (TypeError, ValueError):
                        pass
                if not enabled_queries:
                    enabled_queries = None

        cfg = TPCHConfig(
            db_name=_get("db_name", "tpch"),
            scale_factor=_get("scale_factor", 0.1),
            schema_threads=_get("schema_threads", 4),
            vus=_get("vus", 1),
            refresh_on=_get("refresh_on", False),
            degree_parallel=_get("degree_parallel", 2),
            storage_engine=_get("storage_engine", "innodb"),
            ssl=_get("ssl", False),
            enabled_queries=enabled_queries,
        )
        tier = kwargs.get("tier")
        if tier is not None:
            cfg.db_name = self._derive_tier_db_name(cfg.db_name, str(tier))
        return cfg

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

    def _generate_build_script(
        self,
        host: str,
        port: int,
        config: TPCHConfig
    ) -> str:
        """Generate HammerDB Tcl script for schema building."""
        container_host = self._get_container_host(host)
        return f"""#!/bin/tclsh
dbset db mysql
dbset bm TPC-H
diset connection mysql_host {container_host}
diset connection mysql_port {port}
diset connection mysql_socket null
diset tpch mysql_tpch_user {self.db_user}
diset tpch mysql_tpch_pass {self.db_password}
diset tpch mysql_tpch_dbase {config.db_name}
diset tpch mysql_tpch_storage_engine {config.storage_engine}
diset tpch mysql_scale_fact {config.scale_factor}
diset tpch mysql_num_tpch_threads {config.schema_threads}
buildschema
waittocomplete
"""

    def _generate_run_script(
        self,
        host: str,
        port: int,
        config: TPCHConfig
    ) -> str:
        """Generate HammerDB Tcl script for benchmark run."""
        container_host = self._get_container_host(host)
        return f"""#!/bin/tclsh
dbset db mysql
dbset bm TPC-H
diset connection mysql_host {container_host}
diset connection mysql_port {port}
diset connection mysql_socket null
diset tpch mysql_tpch_user {self.db_user}
diset tpch mysql_tpch_pass {self.db_password}
diset tpch mysql_tpch_dbase {config.db_name}
diset tpch mysql_refresh_on {"true" if config.refresh_on else "false"}
vuset logtotemp 1
vuset vu {config.vus}
vucreate
vurun
waittocomplete
vudestroy
"""

    def _run_hammerdb(
        self,
        script_path: Path,
        log_path: Path,
        timeout_sec: int
    ) -> Dict[str, Any]:
        """Run HammerDB with a Tcl script."""
        cmd = ["docker", "run", "--rm"]

        if self.network_mode == "host":
            cmd += ["--network", "host"]
        else:
            cmd += ["--add-host", "host.docker.internal:host-gateway"]

        script_in_container = f"/scripts/{script_path.name}"
        shell_cmd = (
            'set -e; script="$1"; '
            'run_hammer() { '
            '  if [ -x /home/hammerdb/hammerdbcli ]; then '
            '    /home/hammerdb/hammerdbcli auto "$script"; return; '
            '  fi; '
            '  for d in /home/hammerdb/HammerDB-*; do '
            '    if [ -x "$d/hammerdbcli" ]; then '
            '      cd "$d"; ./hammerdbcli auto "$script"; return; '
            '    fi; '
            '  done; '
            '  echo "hammerdbcli not found under /home/hammerdb" >&2; '
            '  ls -la /home/hammerdb >&2 || true; '
            '  return 127; '
            '}; '
            'run_hammer; rc=$?; '
            'cat /tmp/hdbxtprofile.log 2>/dev/null || true; '
            'exit $rc'
        )

        cmd += [
            "-v", f"{script_path.parent}:/scripts:ro",
            "-w", "/home/hammerdb",
            self.docker_image,
            "sh", "-c", shell_cmd, "sh", script_in_container,
        ]

        result = {
            "command": " ".join(cmd),
            "returncode": -1,
            "output": "",
            "error": None,
        }

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
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
            log_path.write_text(result["output"], encoding="utf-8")

        except Exception as e:
            result["error"] = str(e)
            logger.error(f"HammerDB failed: {e}")

        return result

    def _get_container_host(self, host: str) -> str:
        """Get host address for container."""
        if self.network_mode == "host":
            return host
        if host in ("127.0.0.1", "localhost"):
            return "host.docker.internal"
        return host

    def get_default_config(self) -> Dict[str, Any]:
        """Get default TPC-H configuration."""
        return {
            "docker_image": self.DEFAULT_IMAGE,
            "network_mode": self.DEFAULT_NETWORK_MODE,
            "db_user": "root",
            "db_password": "root",
            "tpch": {
                "db_name": "tpch",
                "scale_factor": 0.1,
                "vus": 1,
            },
        }


# Register the benchmark
from ..registry import register_benchmark
register_benchmark("tpch", TPCHRunner)
