"""
TPC-C Benchmark Runner Implementation

Runs TPC-C (TPROC-C) benchmarks using HammerDB against MySQL-compatible databases.

Supports fine-grained workload reporting:
- schema: Schema creation phase
- data_load: Warehouse data loading phase
- new_order, payment, order_status, delivery, stock_level: Per-transaction-type results
- consistency: Post-run TPC-C consistency condition checks

Multiple VU (virtual user) counts can be specified to test concurrency scaling.
"""

import json
import hashlib
import logging
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Union

from ..base import BenchmarkRunner, BenchmarkResult, BenchmarkStatus
from ._validation import find_success_marker_line, missing_success_marker_error

logger = logging.getLogger(__name__)


# TPC-C output parsing patterns
_TPCC_PATTERNS = {
    "nopm": re.compile(r"System achieved (\d+) NOPM", re.M),
    "tpm": re.compile(r"(\d+)\s+\w*\s*TPM", re.M),
    "active_vus": re.compile(r"Vuser \d+:(\d+) Active Virtual Users", re.M),
    "rampup": re.compile(r"Rampup (\d+) complete", re.M),
}

# HammerDB per-transaction-type result patterns (from timeprofile output)
# Legacy format (HammerDB < v4.9)
_TPCC_TX_PATTERN = re.compile(
    r"Vuser \d+:(\w+) - Loss of Conn (\d+) Timeouts (\d+) Aborts (\d+)",
    re.M,
)
# HammerDB v4.9+ xtprof format: ">>>>> PROC: NEWORD\nCALLS: 34794 ..."
_TPCC_XTPROF_SUMMARY_PATTERN = re.compile(
    r">>>>> SUMMARY OF \d+ ACTIVE VIRTUAL USERS",
    re.M,
)
_TPCC_XTPROF_PROC_PATTERN = re.compile(
    r">>>>> PROC:\s*(\w+)\s*\nCALLS:\s*(\d+)",
    re.M,
)
_TPCC_BUILD_MONITOR_PATTERN = re.compile(r"Vuser\s+(\d+):Monitor Thread", re.I)
_TPCC_BUILD_CREATED_PATTERN = re.compile(r"Vuser\s+(\d+)\s+created\s+-\s+WAIT IDLE", re.I)
_TPCC_BUILD_FINISHED_FAILED_PATTERN = re.compile(r"Vuser\s+(\d+):FINISHED FAILED", re.I)
_TPCC_BUILD_SUCCESS_MARKERS = ("all virtual users complete", "success")

# Maps HammerDB internal transaction names to our workload names
_TPCC_TX_NAME_MAP = {
    "neword": "new_order",
    "payment": "payment",
    "ostat": "order_status",
    "delivery": "delivery",
    "slev": "stock_level",
}

# All supported TPC-C workload names
TPCC_ALL_WORKLOADS = [
    "schema", "data_load",
    "new_order", "payment", "order_status", "delivery", "stock_level",
    "consistency",
]

# Transaction-type workload names (the ones that run per-VU)
TPCC_TX_WORKLOADS = ["new_order", "payment", "order_status", "delivery", "stock_level"]

# TPC-C consistency condition SQL checks (from TPC-C spec section 3.3)
_TPCC_CONSISTENCY_CHECKS = [
    {
        "name": "warehouse_ytd",
        "description": "W_YTD = sum(H_AMOUNT) for each warehouse",
        "query": """
            SELECT w.W_ID, w.W_YTD, COALESCE(SUM(h.H_AMOUNT), 0) as sum_h
            FROM warehouse w LEFT JOIN history h ON w.W_ID = h.H_W_ID
            GROUP BY w.W_ID, w.W_YTD
            HAVING ABS(w.W_YTD - COALESCE(SUM(h.H_AMOUNT), 0)) > 0.01
        """,
    },
    {
        "name": "district_next_oid",
        "description": "D_NEXT_O_ID - 1 = max(O_ID) for each district",
        "query": """
            SELECT d.D_W_ID, d.D_ID, d.D_NEXT_O_ID,
                   COALESCE(MAX(o.O_ID), 0) as max_oid
            FROM district d LEFT JOIN orders o
              ON d.D_W_ID = o.O_W_ID AND d.D_ID = o.O_D_ID
            GROUP BY d.D_W_ID, d.D_ID, d.D_NEXT_O_ID
            HAVING d.D_NEXT_O_ID - 1 != COALESCE(MAX(o.O_ID), 0)
        """,
    },
]


@dataclass
class TPCCConfig:
    """Configuration for TPC-C benchmark."""
    db_name: str = "tpcc"
    warehouses: int = 10
    vus: Any = 8  # int or list[int]
    rampup_min: int = 2
    duration_min: int = 5
    storage_engine: str = "innodb"
    partition: bool = False
    allwarehouse: bool = True
    timeprofile: bool = True
    history_pk: bool = True
    ssl: bool = False
    build_timeout_sec: Optional[int] = None
    build_timeout_ratio: float = 0.8
    enabled_workloads: Optional[List[str]] = None


class TPCCRunner(BenchmarkRunner):
    """
    TPC-C (TPROC-C) benchmark runner for MySQL-compatible databases.

    Uses HammerDB Docker container to run standardized OLTP workloads
    simulating a warehouse order processing system.

    Supports fine-grained workload reporting with per-transaction-type
    results and multiple VU (concurrency) levels.

    Workloads:
    - schema: Schema creation
    - data_load: Warehouse data loading
    - new_order: New Order transactions (per VU count)
    - payment: Payment transactions (per VU count)
    - order_status: Order Status transactions (per VU count)
    - delivery: Delivery transactions (per VU count)
    - stock_level: Stock Level transactions (per VU count)
    - consistency: Post-run TPC-C consistency checks
    """

    name = "tpcc"
    description = "TPC-C (TPROC-C) OLTP benchmark via HammerDB"
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
        return sanitized or "tpcc"

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

    @staticmethod
    def _extract_monitor_vuser(output: str) -> Optional[int]:
        match = _TPCC_BUILD_MONITOR_PATTERN.search(output or "")
        if not match:
            return None
        try:
            return int(match.group(1))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extract_created_vusers(output: str) -> set[int]:
        created = set()
        for match in _TPCC_BUILD_CREATED_PATTERN.finditer(output or ""):
            try:
                created.add(int(match.group(1)))
            except (TypeError, ValueError):
                continue
        return created

    @staticmethod
    def _extract_failed_vusers(output: str) -> set[int]:
        failed = set()
        for match in _TPCC_BUILD_FINISHED_FAILED_PATTERN.finditer(output or ""):
            try:
                failed.add(int(match.group(1)))
            except (TypeError, ValueError):
                continue
        return failed

    @staticmethod
    def _normalize_vus(vus_value: Any) -> List[int]:
        """Normalize vus config to a list of positive ints."""
        if isinstance(vus_value, int):
            return [vus_value] if vus_value > 0 else [1]
        if isinstance(vus_value, list):
            result = []
            for v in vus_value:
                try:
                    iv = int(v)
                    if iv > 0:
                        result.append(iv)
                except (TypeError, ValueError):
                    pass
            return result if result else [1]
        try:
            iv = int(vus_value)
            return [iv] if iv > 0 else [1]
        except (TypeError, ValueError):
            return [1]

    def _parse_build_phases(
        self,
        build_output: str,
        build_returncode: int,
        build_error: Optional[str] = None,
    ) -> Dict[str, str]:
        """Parse build output to determine schema and data_load status."""
        output_lower = (build_output or "").lower()
        failure_line = self._extract_failure_line(build_output)
        timed_out = ((build_error or "").strip().lower() == "timeout" or "[timeout]" in output_lower)

        # Timeout means build phase did not finish reliably; do not award PASS.
        if timed_out:
            return {"schema": "TIMEOUT", "data_load": "TIMEOUT"}

        if build_returncode != 0 or failure_line:
            failed_vusers = self._extract_failed_vusers(build_output)
            monitor_vuser = self._extract_monitor_vuser(build_output)
            created_vusers = self._extract_created_vusers(build_output)

            # If monitor thread fails, schema bootstrap did not finish.
            if monitor_vuser is not None and monitor_vuser in failed_vusers:
                return {"schema": "FAIL", "data_load": "FAIL"}

            # If every created VU failed, treat build as full failure.
            if created_vusers and failed_vusers and created_vusers.issubset(failed_vusers):
                return {"schema": "FAIL", "data_load": "FAIL"}

            # Try to determine which phase failed
            # If the failure mentions table creation, schema failed
            if failure_line:
                fl = failure_line.lower()
                if any(kw in fl for kw in ("create table", "create index", "alter table")):
                    return {"schema": "FAIL", "data_load": "SKIP"}

            # If we see loading progress but then failure, schema passed but load failed
            if any(p in output_lower for p in ("loading warehouse", "worker ")):
                return {"schema": "PASS", "data_load": "FAIL"}

            # Otherwise both failed — no keyword matched, log for observability
            logger.warning(
                "TPC-C build phase could not be determined; returncode=%d, failure_line=%r",
                build_returncode, failure_line,
            )
            return {"schema": "FAIL", "data_load": "FAIL"}

        # Build succeeded overall only when it also emits positive completion evidence.
        if not find_success_marker_line(build_output, _TPCC_BUILD_SUCCESS_MARKERS):
            logger.warning(
                "TPC-C build returned 0 but output lacks success markers (returncode=%d)",
                build_returncode,
            )
            return {"schema": "FAIL", "data_load": "FAIL"}
        return {"schema": "PASS", "data_load": "PASS"}

    def _resolve_build_timeout(self, config: TPCCConfig, remaining_sec: float) -> int:
        """Resolve timeout for build phase from explicit seconds or ratio."""
        remaining = max(1, int(remaining_sec))

        explicit_timeout = config.build_timeout_sec
        try:
            if explicit_timeout is not None:
                explicit_timeout = int(explicit_timeout)
            if explicit_timeout and explicit_timeout > 0:
                return min(remaining, explicit_timeout)
        except (TypeError, ValueError):
            pass

        try:
            ratio = float(config.build_timeout_ratio)
        except (TypeError, ValueError):
            ratio = 0.8
        ratio = min(1.0, max(0.1, ratio))
        return max(1, int(remaining * ratio))

    def _parse_transaction_results(self, run_output: str) -> Dict[str, Dict[str, Any]]:
        """Parse per-transaction-type results from HammerDB timeprofile output.

        Supports two formats:
        - Legacy (< v4.9): "Vuser N:neword - Loss of Conn 0 Timeouts 0 Aborts 0"
        - xtprof (v4.9+): SUMMARY section with ">>>>> PROC: NEWORD\\nCALLS: N ..."

        Returns dict mapping our workload names to their stats.
        """
        results = {}

        # Try legacy format first
        for match in _TPCC_TX_PATTERN.finditer(run_output or ""):
            hammerdb_name = match.group(1).lower()
            workload_name = _TPCC_TX_NAME_MAP.get(hammerdb_name)
            if not workload_name:
                continue

            loss_of_conn = int(match.group(2))
            timeouts = int(match.group(3))
            aborts = int(match.group(4))

            if workload_name in results:
                results[workload_name]["loss_of_conn"] += loss_of_conn
                results[workload_name]["timeouts"] += timeouts
                results[workload_name]["aborts"] += aborts
            else:
                results[workload_name] = {
                    "loss_of_conn": loss_of_conn,
                    "timeouts": timeouts,
                    "aborts": aborts,
                }

        if results:
            # Determine pass/fail from legacy error counters
            for wl_name, stats in results.items():
                if stats["timeouts"] > 0 or stats["aborts"] > 0 or stats["loss_of_conn"] > 0:
                    stats["status"] = "FAIL"
                else:
                    stats["status"] = "PASS"
            return results

        # Fall back to xtprof SUMMARY format (HammerDB v4.9+)
        summary_match = _TPCC_XTPROF_SUMMARY_PATTERN.search(run_output or "")
        if not summary_match:
            return results

        summary_text = (run_output or "")[summary_match.start():]
        for match in _TPCC_XTPROF_PROC_PATTERN.finditer(summary_text):
            proc_name = match.group(1).lower()
            calls = int(match.group(2))
            workload_name = _TPCC_TX_NAME_MAP.get(proc_name)
            if not workload_name:
                continue
            results[workload_name] = {
                "calls": calls,
                "status": "PASS" if calls > 0 else "FAIL",
            }

        return results

    def _run_consistency_checks(self, host: str, port: int, db_name: str) -> str:
        """Run TPC-C consistency condition checks. Returns 'PASS', 'FAIL', 'SKIP', or 'ERROR'."""
        try:
            import pymysql
        except ImportError:
            logger.warning("pymysql not installed; skipping TPC-C consistency checks")
            return "SKIP"

        db_name_safe = self._sanitize_db_name(db_name)
        conn = None
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                conn = pymysql.connect(
                    host=host,
                    port=port,
                    user=self.db_user,
                    password=self.db_password,
                    database=db_name_safe,
                    connect_timeout=10,
                )
                break
            except Exception as e:
                logger.warning(
                    "TPC-C consistency connect attempt %d/%d failed: %s",
                    attempt, max_attempts, e,
                )
                if attempt < max_attempts:
                    time.sleep(2)
                else:
                    logger.error("TPC-C consistency checks failed: unable to connect after %d attempts", max_attempts)
                    return "ERROR"

        try:
            all_pass = True
            for check in _TPCC_CONSISTENCY_CHECKS:
                try:
                    with conn.cursor() as cur:
                        cur.execute(check["query"])
                        violations = cur.fetchall()
                        if violations:
                            logger.warning(
                                f"TPC-C consistency check '{check['name']}' "
                                f"found {len(violations)} violation(s)"
                            )
                            all_pass = False
                except Exception as e:
                    err_msg = str(e).lower()
                    if "doesn't exist" in err_msg or "unknown column" in err_msg:
                        logger.warning(
                            "TPC-C consistency check '%s' skipped (schema mismatch): %s",
                            check["name"], e,
                        )
                        return "SKIP"
                    logger.warning(f"TPC-C consistency check '{check['name']}' error: {e}")
                    all_pass = False
            return "PASS" if all_pass else "FAIL"
        except Exception as e:
            logger.error(f"TPC-C consistency checks failed: {e}")
            return "ERROR"
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    def run(
        self,
        sut_host: str,
        sut_port: int,
        output_dir: Path,
        timeout_sec: int = 1800,
        **kwargs
    ) -> BenchmarkResult:
        """
        Run TPC-C benchmark with fine-grained workload reporting.

        Execution phases:
        1. Build: Schema creation + data loading (one-time)
        2. Run: Execute TPC-C workload for each VU count
        3. Consistency: Post-run consistency checks
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir = output_dir / "raw" / "tpcc"
        raw_dir.mkdir(parents=True, exist_ok=True)
        scripts_dir = output_dir / "scripts" / "tpcc"
        scripts_dir.mkdir(parents=True, exist_ok=True)

        start_time = time.time()

        if self.config.get("enabled") is False:
            return BenchmarkResult(
                status=BenchmarkStatus.SKIPPED,
                details="TPC-C disabled by config",
                output_dir=output_dir,
                elapsed_sec=time.time() - start_time,
            )

        # Get TPC-C configuration
        tpcc_config = self._get_config(kwargs)
        vus_list = self._normalize_vus(tpcc_config.vus)
        enabled = tpcc_config.enabled_workloads or list(TPCC_ALL_WORKLOADS)

        workload_results: Dict[str, str] = {}
        all_metrics: Dict[str, Any] = {}
        run_details: List[Dict[str, Any]] = []
        first_error: Optional[str] = None

        # Ensure database exists
        db_create_ok = self._ensure_database(sut_host, sut_port, tpcc_config.db_name)
        if not db_create_ok:
            for wl in enabled:
                workload_results[wl] = "ERROR"
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error="Failed to create database",
                output_dir=output_dir,
                elapsed_sec=time.time() - start_time,
                workload_results=workload_results,
            )

        # ── Phase 1: Build schema ──
        build_script = self._generate_build_script(sut_host, sut_port, tpcc_config)
        build_script_path = scripts_dir / "tpcc_build.tcl"
        build_script_path.write_text(build_script, encoding="utf-8")

        logger.info("Running TPC-C schema build...")
        remaining = timeout_sec - (time.time() - start_time)
        build_timeout = self._resolve_build_timeout(tpcc_config, remaining)
        build_result = self._run_hammerdb(
            build_script_path,
            raw_dir / "tpcc_build.log",
            build_timeout,
        )

        build_output = build_result.get("output", "") or ""
        build_phases = self._parse_build_phases(
            build_output,
            build_result["returncode"],
            build_result.get("error"),
        )

        if "schema" in enabled:
            workload_results["schema"] = build_phases["schema"]
        if "data_load" in enabled:
            workload_results["data_load"] = build_phases["data_load"]

        build_failed = (
            build_phases["schema"] not in ("PASS", "SKIP")
            or build_phases["data_load"] not in ("PASS", "SKIP")
        )
        if build_failed:
            first_error = (
                "TPC-C build failed: "
                f"{self._extract_failure_line(build_output) or build_result.get('error') or missing_success_marker_error('TPC-C build', _TPCC_BUILD_SUCCESS_MARKERS)}"
            )
            # Skip all remaining workloads
            for wl in enabled:
                if wl not in workload_results:
                    wl_keys = self._expand_tx_workload_keys(wl, vus_list, enabled)
                    for key in wl_keys:
                        workload_results[key] = "SKIP"

            expected = self.planned_workload_count(tpcc={"vus": vus_list, "enabled_workloads": enabled})
            if len(workload_results) != expected:
                logger.warning("TPC-C workload count mismatch: expected %d, got %d", expected, len(workload_results))

            self._write_results_file(output_dir, tpcc_config, vus_list, all_metrics,
                                     build_result, run_details, workload_results)
            return self._make_result(
                workload_results, all_metrics, first_error, build_output,
                output_dir, start_time,
            )

        # ── Phase 2: Run benchmark for each VU count ──
        tx_workloads_enabled = any(wl in enabled for wl in TPCC_TX_WORKLOADS)
        if not tx_workloads_enabled:
            logger.info("TPC-C tx workloads not enabled; skipping run phase")

        run_vus_list = vus_list if tx_workloads_enabled else []
        for vu_count in run_vus_list:
            remaining = timeout_sec - (time.time() - start_time)
            if remaining <= 0:
                # Mark remaining VU workloads as TIMEOUT
                for tx_wl in TPCC_TX_WORKLOADS:
                    if tx_wl not in enabled:
                        continue
                    key = self._make_tx_workload_key(tx_wl, vu_count, vus_list)
                    workload_results[key] = "TIMEOUT"
                continue

            run_script = self._generate_run_script(sut_host, sut_port, tpcc_config, vus=vu_count)
            run_script_path = scripts_dir / f"tpcc_run_vus_{vu_count}.tcl"
            run_script_path.write_text(run_script, encoding="utf-8")

            logger.info(f"Running TPC-C benchmark with {vu_count} VUs...")
            run_result = self._run_hammerdb(
                run_script_path,
                raw_dir / f"tpcc_run_vus_{vu_count}.log",
                max(1, int(remaining)),
            )

            run_output = run_result.get("output", "") or ""
            run_failure = self._extract_failure_line(run_output)
            metrics = self.parse_results(run_output)
            tx_results = self._parse_transaction_results(run_output)

            vu_key = f"vus_{vu_count}"
            all_metrics[vu_key] = {
                "nopm": metrics.get("nopm", 0),
                "tpm": metrics.get("tpm", 0),
                "transactions": tx_results,
            }
            run_details.append({
                "vus": vu_count,
                "result": run_result,
                "metrics": metrics,
                "tx_results": tx_results,
            })

            # Overall run failure for this VU count
            run_failed = (run_result["returncode"] != 0 or run_failure)

            for tx_wl in TPCC_TX_WORKLOADS:
                if tx_wl not in enabled:
                    continue
                key = self._make_tx_workload_key(tx_wl, vu_count, vus_list)
                if run_failed:
                    workload_results[key] = "FAIL"
                    if first_error is None:
                        first_error = run_failure or run_result.get("error") or "TPC-C run failed"
                elif tx_wl in tx_results:
                    workload_results[key] = tx_results[tx_wl]["status"]
                elif metrics.get("nopm", 0) > 0:
                    # Do not award PASS without per-transaction evidence.
                    if tx_wl == TPCC_TX_WORKLOADS[0]:
                        logger.warning(
                            "TPC-C VUs=%d: NOPM=%d but no timeprofile data; "
                            "all tx workloads will default to FAIL",
                            vu_count, metrics["nopm"],
                        )
                    workload_results[key] = "FAIL"
                    if first_error is None:
                        first_error = (
                            f"TPC-C VUs={vu_count}: missing transaction profile data"
                        )
                else:
                    workload_results[key] = "FAIL"
                    if first_error is None:
                        first_error = "TPC-C: NOPM is 0"

        # ── Phase 3: Consistency checks ──
        if "consistency" in enabled:
            remaining = timeout_sec - (time.time() - start_time)
            if remaining > 0:
                logger.info("Running TPC-C consistency checks...")
                workload_results["consistency"] = self._run_consistency_checks(
                    sut_host, sut_port, tpcc_config.db_name,
                )
            else:
                workload_results["consistency"] = "TIMEOUT"

        expected = self.planned_workload_count(tpcc={"vus": vus_list, "enabled_workloads": enabled})
        if len(workload_results) != expected:
            logger.warning("TPC-C workload count mismatch: expected %d, got %d", expected, len(workload_results))

        self._write_results_file(output_dir, tpcc_config, vus_list, all_metrics,
                                 build_result, run_details, workload_results)

        return self._make_result(
            workload_results, all_metrics, first_error, "",
            output_dir, start_time,
        )

    def _make_tx_workload_key(self, tx_name: str, vu_count: int, vus_list: List[int]) -> str:
        """Generate workload key for a transaction type, adding VU suffix if multiple VUs."""
        if len(vus_list) > 1:
            return f"{tx_name}:vus_{vu_count}"
        return tx_name

    def _expand_tx_workload_keys(
        self, wl_name: str, vus_list: List[int], enabled: List[str]
    ) -> List[str]:
        """Expand a workload name to all its keys (handling per-VU expansion)."""
        if wl_name in TPCC_TX_WORKLOADS:
            return [self._make_tx_workload_key(wl_name, vu, vus_list) for vu in vus_list]
        return [wl_name]

    def _make_result(
        self,
        workload_results: Dict[str, str],
        all_metrics: Dict[str, Any],
        first_error: Optional[str],
        raw_output: str,
        output_dir: Path,
        start_time: float,
    ) -> BenchmarkResult:
        """Build the final BenchmarkResult from workload results."""
        elapsed = time.time() - start_time

        # Determine overall status
        statuses = set(workload_results.values())
        non_pass = statuses - {"PASS", "SKIP"}
        if not non_pass:
            overall = BenchmarkStatus.ACCEPTED
        elif non_pass <= {"TIMEOUT"}:
            overall = BenchmarkStatus.TIME_LIMIT_EXCEEDED
        else:
            overall = BenchmarkStatus.WRONG_ANSWER

        # Calculate score: average NOPM across all VU runs
        nopm_values = []
        for vu_key, vu_metrics in all_metrics.items():
            if isinstance(vu_metrics, dict):
                nopm = vu_metrics.get("nopm", 0)
                if nopm > 0:
                    nopm_values.append(nopm)
        score = sum(nopm_values) / len(nopm_values) if nopm_values else 0.0

        # Build details string
        pass_count = sum(1 for s in workload_results.values() if s == "PASS")
        total = len(workload_results)
        failed = [k for k, v in workload_results.items() if v not in ("PASS", "SKIP")]
        details = f"TPC-C: {pass_count}/{total} workloads passed"
        if failed:
            details += f" (failed: {', '.join(sorted(failed))})"

        return BenchmarkResult(
            status=overall,
            score=score,
            metrics=all_metrics,
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
        config: "TPCCConfig",
        vus_list: List[int],
        all_metrics: Dict[str, Any],
        build_result: Dict[str, Any],
        run_details: List[Dict[str, Any]],
        workload_results: Dict[str, str],
    ) -> None:
        """Write tpcc_results.json."""
        try:
            results_file = output_dir / "tpcc_results.json"
            results_file.write_text(
                json.dumps({
                    "config": {
                        "warehouses": config.warehouses,
                        "vus": vus_list,
                        "duration_min": config.duration_min,
                        "enabled_workloads": config.enabled_workloads,
                    },
                    "metrics": all_metrics,
                    "workload_results": workload_results,
                    "build": build_result,
                    "runs": run_details,
                }, indent=2, default=str),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning(f"Failed to write tpcc_results.json: {e}")

    def parse_results(self, output: str) -> Dict[str, Any]:
        """Parse TPC-C output for NOPM/TPM metrics."""
        metrics = {}
        for key, pattern in _TPCC_PATTERNS.items():
            match = pattern.search(output)
            if match:
                metrics[key] = int(match.group(1))
        return metrics

    def planned_workload_count(self, **kwargs) -> int:
        """Return the expected number of workload result entries."""
        tpcc_config = self._get_config(kwargs)
        enabled = tpcc_config.enabled_workloads or list(TPCC_ALL_WORKLOADS)
        vus_list = self._normalize_vus(tpcc_config.vus)

        count = 0
        for wl in enabled:
            if wl in TPCC_TX_WORKLOADS:
                count += len(vus_list)
            else:
                count += 1
        return max(1, count)

    def _get_config(self, kwargs: Dict[str, Any]) -> TPCCConfig:
        """Get TPC-C configuration.

        Supports both:
        - nested config: {"tpcc": {...}}
        - flat config: {"warehouses": ..., "vus": ...}
        """
        tpcc = kwargs.get("tpcc")
        if not isinstance(tpcc, dict):
            tpcc = self.config.get("tpcc")
        if not isinstance(tpcc, dict):
            tpcc = {}

        def _get(key: str, default: Any) -> Any:
            if key in tpcc:
                return tpcc.get(key, default)
            return self.config.get(key, default)

        cfg = TPCCConfig(
            db_name=_get("db_name", "tpcc"),
            warehouses=_get("warehouses", 1),
            vus=_get("vus", 4),
            rampup_min=_get("rampup_min", 1),
            duration_min=_get("duration_min", 2),
            storage_engine=_get("storage_engine", "innodb"),
            partition=_get("partition", False),
            allwarehouse=_get("allwarehouse", True),
            timeprofile=_get("timeprofile", True),
            history_pk=_get("history_pk", True),
            ssl=_get("ssl", False),
            build_timeout_sec=_get("build_timeout_sec", None),
            build_timeout_ratio=_get("build_timeout_ratio", 0.8),
            enabled_workloads=_get("enabled_workloads", None),
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
        config: TPCCConfig
    ) -> str:
        """Generate HammerDB Tcl script for schema building."""
        container_host = self._get_container_host(host)
        warehouses = config.warehouses
        return f"""#!/bin/tclsh
dbset db mysql
dbset bm TPC-C
diset connection mysql_host {container_host}
diset connection mysql_port {port}
diset connection mysql_socket null
diset tpcc mysql_user {self.db_user}
diset tpcc mysql_pass {self.db_password}
diset tpcc mysql_dbase {config.db_name}
diset tpcc mysql_storage_engine {config.storage_engine}
diset tpcc mysql_partition {"true" if config.partition else "false"}
diset tpcc mysql_count_ware {warehouses}
diset tpcc mysql_num_vu {min(warehouses, 4)}
buildschema
waittocomplete
"""

    def _generate_run_script(
        self,
        host: str,
        port: int,
        config: TPCCConfig,
        vus: Optional[int] = None,
    ) -> str:
        """Generate HammerDB Tcl script for benchmark run."""
        container_host = self._get_container_host(host)
        vu_count = vus if vus is not None else self._normalize_vus(config.vus)[0]
        return f"""#!/bin/tclsh
dbset db mysql
dbset bm TPC-C
diset connection mysql_host {container_host}
diset connection mysql_port {port}
diset connection mysql_socket null
diset tpcc mysql_user {self.db_user}
diset tpcc mysql_pass {self.db_password}
diset tpcc mysql_dbase {config.db_name}
diset tpcc mysql_driver timed
diset tpcc mysql_rampup {config.rampup_min}
diset tpcc mysql_duration {config.duration_min}
diset tpcc mysql_allwarehouse {"true" if config.allwarehouse else "false"}
diset tpcc mysql_timeprofile {"true" if config.timeprofile else "false"}
vuset logtotemp 1
vuset vu {vu_count}
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
        """Get default TPC-C configuration."""
        return {
            "docker_image": self.DEFAULT_IMAGE,
            "network_mode": self.DEFAULT_NETWORK_MODE,
            "db_user": "root",
            "db_password": "root",
            "tpcc": {
                "db_name": "tpcc",
                "warehouses": 1,
                "vus": [4],
                "rampup_min": 1,
                "duration_min": 2,
                "build_timeout_ratio": 0.8,
            },
        }


# Register the benchmark
from ..registry import register_benchmark
register_benchmark("tpcc", TPCCRunner)
