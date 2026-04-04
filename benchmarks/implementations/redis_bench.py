"""
Redis KV Store Benchmark Runner Implementation

Runs Redis-compatible benchmarks against KV store implementations.

Four benchmark suites, mapped to progressive tiers (L0-L6):
  - tcl:              Frozen Redis TCL test subset (protocol correctness)
  - redis_benchmark:  redis-benchmark CLI (throughput smoke test)
  - ycsb:             YCSB Redis binding (application workloads)
  - memtier:          memtier_benchmark (high-pressure stress test)

Tier mapping when per-tier suites are configured via config YAML:
  L0      → tcl only
  L1      → tcl + redis_benchmark (set, get, incr)
  L2      → tcl + redis_benchmark (full command set)
  L3      → tcl only (persistence + pubsub)
  L4      → tcl + redis_benchmark (pipeline)
  L5      → ycsb (workloads a-f)
  L6      → tcl + ycsb + memtier
"""

from __future__ import annotations

import json
import logging
import os
import re
import shlex
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..base import BenchmarkResult, BenchmarkRunner, BenchmarkStatus
from .redis_conformance import RedisCaseFailure, run_redis_case

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RULESET_DIR = "./benchmarks/rulesets"
BENCHMARK_RULESET_DIR = PROJECT_ROOT / "benchmarks" / "rulesets"

# ---------------------------------------------------------------------------
# Redis-benchmark test definitions: (workload_id, redis-benchmark -t argument)
# ---------------------------------------------------------------------------
REDIS_BENCHMARK_TESTS_L1: List[Tuple[str, str]] = [
    ("redis_benchmark:set", "set"),
    ("redis_benchmark:get", "get"),
    ("redis_benchmark:incr", "incr"),
]

REDIS_BENCHMARK_TESTS_L2: List[Tuple[str, str]] = [
    ("redis_benchmark:ping_inline", "ping_inline"),
    ("redis_benchmark:ping_mbulk", "ping_mbulk"),
    ("redis_benchmark:set", "set"),
    ("redis_benchmark:get", "get"),
    ("redis_benchmark:incr", "incr"),
    ("redis_benchmark:lpush", "lpush"),
    ("redis_benchmark:rpush", "rpush"),
    ("redis_benchmark:lpop", "lpop"),
    ("redis_benchmark:rpop", "rpop"),
    ("redis_benchmark:sadd", "sadd"),
    ("redis_benchmark:hset", "hset"),
    ("redis_benchmark:spop", "spop"),
    ("redis_benchmark:zadd", "zadd"),
    ("redis_benchmark:zpopmin", "zpopmin"),
    ("redis_benchmark:lrange_100", "lrange_100"),
    ("redis_benchmark:lrange_300", "lrange_300"),
    ("redis_benchmark:lrange_500", "lrange_500"),
    ("redis_benchmark:lrange_600", "lrange_600"),
    ("redis_benchmark:mset_10", "mset"),
]

REDIS_BENCHMARK_TESTS_L4: List[Tuple[str, str]] = [
    ("redis_benchmark:pipeline_16", "set"),  # uses -P 16
]

REDIS_BENCHMARK_CONFIG_ALIASES: Dict[str, Tuple[str, str]] = {
    "mset_10": ("redis_benchmark:mset_10", "mset"),
    "pipeline_16": ("redis_benchmark:pipeline_16", "set"),
}

# YCSB workloads
YCSB_WORKLOADS: List[Tuple[str, str]] = [
    ("ycsb:a", "a"),
    ("ycsb:b", "b"),
    ("ycsb:c", "c"),
    ("ycsb:d", "d"),
    ("ycsb:e", "e"),
    ("ycsb:f", "f"),
]

# Memtier scenarios: (workload_id, extra_args)
MEMTIER_SCENARIOS: List[Tuple[str, str]] = [
    ("memtier:base", "--ratio=1:1 --key-pattern=R:R -n 10000 -c 10 -t 2"),
    ("memtier:large_value", "--ratio=1:1 --key-pattern=R:R -n 5000 -c 5 -t 2 --data-size=4096"),
    ("memtier:pipeline_16", "--ratio=1:1 --key-pattern=R:R -n 10000 -c 10 -t 2 --pipeline=16"),
]

SUPPORTED_SUITES: Tuple[str, ...] = ("tcl", "redis_benchmark", "ycsb", "memtier")

# Regex for parsing redis-benchmark --csv output
REDIS_BENCH_CSV_RE = re.compile(
    r'"(?P<test>[^"]+)","(?P<rps>[0-9.]+)","(?P<avg>[0-9.]+)","(?P<min>[0-9.]+)",'
    r'"(?P<p50>[0-9.]+)","(?P<p95>[0-9.]+)","(?P<p99>[0-9.]+)","(?P<max>[0-9.]+)"'
)
REDIS_BENCH_CSV_HEADER = (
    '"test","rps","avg_latency_ms","min_latency_ms","p50_latency_ms",'
    '"p95_latency_ms","p99_latency_ms","max_latency_ms"'
)

# YCSB output parsing
YCSB_THROUGHPUT_RE = re.compile(r"\[OVERALL\],\s*Throughput\(ops/sec\),\s*([0-9.]+)")
YCSB_ERROR_RE = re.compile(r"\[(?:INSERT|READ|UPDATE|SCAN|DELETE)\],\s*Return=ERROR,\s*(\d+)")
YCSB_WARNING_LINE_RE = re.compile(r"^(?:WARNING:|WARN(?:ING)?\b)")
YCSB_ERROR_LINE_RE = re.compile(
    r"(?:\bReturn=ERROR\b|Exception:|Exception in thread|Error from server:|\bERR\b)"
)

# Memtier summary line
MEMTIER_TOTALS_RE = re.compile(
    r"Totals\s+(?P<ops>[0-9.]+)\s+(?P<hits>[0-9.]+)\s+(?P<misses>[0-9.]+)\s+"
    r"(?P<avg_latency>[0-9.]+)\s+(?P<p50_latency>[0-9.]+)\s+(?P<p99_latency>[0-9.]+)"
)
MEMTIER_PROGRESS_RE = re.compile(
    r"\[RUN #\d+[^\n]*\]\s+\d+\s+threads:\s+\d+\s+ops,\s+\d+\s+\(avg:\s*(?P<ops>[0-9.]+)\)\s+ops/sec,"
    r".*?\(avg:\s*(?P<avg_latency>[0-9.]+)\)\s+msec latency",
    re.DOTALL,
)
MEMTIER_WARNING_LINE_RE = re.compile(r"^(?:WARNING:|WARN(?:ING)?\b)")
MEMTIER_ERROR_LINE_RE = re.compile(r"(?:^ERROR:|^Error:|Exception|Traceback|Error from server:|\bERR\b)")


@dataclass
class RedisBenchConfig:
    """Configuration for the Redis KV Store benchmark runner."""

    network_mode: str = "host"
    suites: List[str] = field(default_factory=list)
    # TCL
    tcl_repo: str = "https://github.com/redis/redis.git"
    tcl_repo_ref: str = "7.2.4"
    tcl_patch_dir: str = "./benchmarks/implementations/redis_tcl_patches"
    tcl_ruleset: str = ""
    ruleset_dir: str = DEFAULT_RULESET_DIR
    # redis-benchmark
    redis_benchmark_image: str = "redis:7.2.4-alpine"
    redis_benchmark_tests: List[str] = field(default_factory=list)
    # YCSB
    ycsb_runner_image: str = "hackathon-24h-bench/ycsb-runner:0.17.0-temurin11"
    ycsb_runner_dockerfile: str = "./benchmarks/implementations/docker/ycsb_runner/Dockerfile"
    ycsb_runner_context: str = "./benchmarks/implementations/docker/ycsb_runner"
    ycsb_base_image: str = "eclipse-temurin:11-jre-jammy"
    ycsb_release_url: str = (
        "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
        "ycsb-redis-binding-0.17.0.tar.gz"
    )
    ycsb_release_fallback_url: str = (
        "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
        "ycsb-0.17.0.tar.gz"
    )
    ycsb_datatype: str = "string"
    ycsb_workloads: List[str] = field(default_factory=list)
    # memtier
    memtier_docker_image: str = "redislabs/memtier_benchmark:2.1.0"
    memtier_scenarios: List[str] = field(default_factory=list)


class RedisBenchRunner(BenchmarkRunner):
    """Redis KV Store benchmark runner (tcl / redis_benchmark / ycsb / memtier)."""

    name = "redis_bench"
    description = "Redis KV Store benchmark (TCL, redis-benchmark, YCSB, memtier)"
    supported_suts = ["redis_kvstore"]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

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
        unknown = sorted({s for s in suites if s not in SUPPORTED_SUITES})
        if unknown:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error=(
                    f"Unsupported redis_bench suite(s): {', '.join(unknown)}. "
                    f"Supported suites: {', '.join(SUPPORTED_SUITES)}"
                ),
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )
        if not suites:
            elapsed = time.time() - start_time
            return BenchmarkResult(
                status=BenchmarkStatus.RUNTIME_ERROR,
                error="No enabled suites in redis_bench config",
                output_dir=output_dir,
                elapsed_sec=elapsed,
            )

        workload_results: Dict[str, str] = {}
        all_metrics: Dict[str, Any] = {}
        all_errors: List[str] = []

        if "tcl" in suites:
            logger.info("Running redis_bench suite: tcl")
            tcl_dir = raw_dir / "tcl"
            tcl_dir.mkdir(parents=True, exist_ok=True)
            tcl_results, tcl_metrics = self._run_tcl_suite(
                sut_host, sut_port, bench_config, tcl_dir, benchmark_deadline,
            )
            workload_results.update(tcl_results)
            all_metrics.update(tcl_metrics)

        if "redis_benchmark" in suites:
            logger.info("Running redis_bench suite: redis_benchmark")
            rb_dir = raw_dir / "redis_benchmark"
            rb_dir.mkdir(parents=True, exist_ok=True)
            rb_results, rb_metrics = self._run_redis_benchmark_suite(
                sut_host, sut_port, bench_config, rb_dir, benchmark_deadline, tier,
            )
            workload_results.update(rb_results)
            all_metrics.update(rb_metrics)

        if "ycsb" in suites:
            logger.info("Running redis_bench suite: ycsb")
            ycsb_dir = raw_dir / "ycsb"
            ycsb_dir.mkdir(parents=True, exist_ok=True)
            ycsb_results, ycsb_metrics = self._run_ycsb_suite(
                sut_host, sut_port, bench_config, ycsb_dir, benchmark_deadline,
            )
            workload_results.update(ycsb_results)
            all_metrics.update(ycsb_metrics)

        if "memtier" in suites:
            logger.info("Running redis_bench suite: memtier")
            mt_dir = raw_dir / "memtier"
            mt_dir.mkdir(parents=True, exist_ok=True)
            mt_results, mt_metrics = self._run_memtier_suite(
                sut_host, sut_port, bench_config, mt_dir, benchmark_deadline,
            )
            workload_results.update(mt_results)
            all_metrics.update(mt_metrics)

        elapsed = time.time() - start_time

        # Check if we exceeded the deadline
        if time.time() > benchmark_deadline and not workload_results:
            return BenchmarkResult(
                status=BenchmarkStatus.TIME_LIMIT_EXCEEDED,
                error="Benchmark timeout exhausted",
                output_dir=output_dir,
                elapsed_sec=elapsed,
                workload_results=workload_results,
                metrics=all_metrics,
            )

        # Determine overall status and score
        score = self._calculate_score(workload_results)
        if not workload_results:
            status = BenchmarkStatus.RUNTIME_ERROR
        elif all(v == "PASS" for v in workload_results.values()):
            status = BenchmarkStatus.ACCEPTED
        elif any(v == "TIMEOUT" for v in workload_results.values()):
            status = BenchmarkStatus.TIME_LIMIT_EXCEEDED
        else:
            status = BenchmarkStatus.WRONG_ANSWER

        # Save summary
        summary_file = output_dir / "redis_bench_results.json"
        try:
            summary_file.write_text(json.dumps({
                "workload_results": workload_results,
                "metrics": all_metrics,
                "score": score,
                "elapsed_sec": elapsed,
            }, indent=2, default=str))
        except Exception as e:
            logger.warning(f"Failed to write summary: {e}")

        return BenchmarkResult(
            status=status,
            score=score,
            metrics=all_metrics,
            details=f"redis_bench: {sum(1 for v in workload_results.values() if v == 'PASS')}/{len(workload_results)} workloads passed",
            output_dir=output_dir,
            elapsed_sec=elapsed,
            workload_results=workload_results,
        )

    def parse_results(self, output: str) -> Dict[str, Any]:
        return {}

    def planned_workload_count(self, **kwargs) -> int:
        tier = str(kwargs.get("tier") or "").strip()
        cfg = self._get_config(kwargs)
        suites = self._select_suites(cfg, tier=tier)
        count = 0
        if "tcl" in suites:
            count += self._tcl_workload_count(cfg)
        if "redis_benchmark" in suites:
            count += len(self._redis_benchmark_tests_for_tier(cfg, tier))
        if "ycsb" in suites:
            count += len(self._ycsb_workloads(cfg))
        if "memtier" in suites:
            count += len(self._memtier_scenarios(cfg))
        return max(count, 1)

    def planned_workload_ids(self, **kwargs) -> List[str]:
        tier = str(kwargs.get("tier") or "").strip()
        cfg = self._get_config(kwargs)
        suites = self._select_suites(cfg, tier=tier)
        ids: List[str] = []
        if "tcl" in suites:
            ids.extend(self._tcl_workload_ids(cfg))
        if "redis_benchmark" in suites:
            ids.extend(wid for wid, _ in self._redis_benchmark_tests_for_tier(cfg, tier))
        if "ycsb" in suites:
            ids.extend(wid for wid, _ in self._ycsb_workloads(cfg))
        if "memtier" in suites:
            ids.extend(wid for wid, _ in self._memtier_scenarios(cfg))
        return ids

    def get_default_config(self) -> Dict[str, Any]:
        return {
            "redis_bench": {
                "network_mode": "host",
                "ruleset_dir": DEFAULT_RULESET_DIR,
                "tcl_repo": "https://github.com/redis/redis.git",
                "tcl_repo_ref": "7.2.4",
                "redis_benchmark_image": "redis:7.2.4-alpine",
                "ycsb_runner_image": "hackathon-24h-bench/ycsb-runner:0.17.0-temurin11",
                "ycsb_runner_dockerfile": "./benchmarks/implementations/docker/ycsb_runner/Dockerfile",
                "ycsb_runner_context": "./benchmarks/implementations/docker/ycsb_runner",
                "ycsb_base_image": "eclipse-temurin:11-jre-jammy",
                "ycsb_release_url": (
                    "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
                    "ycsb-redis-binding-0.17.0.tar.gz"
                ),
                "memtier_docker_image": "redislabs/memtier_benchmark:2.1.0",
            }
        }

    # ------------------------------------------------------------------
    # Config handling
    # ------------------------------------------------------------------

    def _get_config(self, kwargs: Dict[str, Any]) -> RedisBenchConfig:
        cfg = kwargs.get("redis_bench")
        if not isinstance(cfg, dict):
            cfg = self.config.get("redis_bench")
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

        rb_tests = _get("redis_benchmark_tests", [])
        if isinstance(rb_tests, list):
            rb_tests = [str(t).strip() for t in rb_tests if str(t).strip()]
        else:
            rb_tests = []

        ycsb_wl = _get("ycsb_workloads", [])
        if isinstance(ycsb_wl, list):
            ycsb_wl = [str(w).strip() for w in ycsb_wl if str(w).strip()]
        else:
            ycsb_wl = []

        mt_scen = _get("memtier_scenarios", [])
        if isinstance(mt_scen, list):
            mt_scen = [str(s).strip() for s in mt_scen if str(s).strip()]
        else:
            mt_scen = []

        return RedisBenchConfig(
            network_mode=str(_get("network_mode", "host")),
            suites=suites,
            tcl_repo=str(_get("tcl_repo", "https://github.com/redis/redis.git")),
            tcl_repo_ref=str(_get("tcl_repo_ref", "7.2.4")),
            tcl_patch_dir=str(_get("tcl_patch_dir", "./benchmarks/implementations/redis_tcl_patches")),
            tcl_ruleset=str(_get("tcl_ruleset", "")),
            ruleset_dir=str(_get("ruleset_dir", DEFAULT_RULESET_DIR)),
            redis_benchmark_image=str(_get("redis_benchmark_image", "redis:7.2.4-alpine")),
            redis_benchmark_tests=rb_tests,
            ycsb_runner_image=str(_get("ycsb_runner_image", "hackathon-24h-bench/ycsb-runner:0.17.0-temurin11")),
            ycsb_runner_dockerfile=str(_get(
                "ycsb_runner_dockerfile",
                "./benchmarks/implementations/docker/ycsb_runner/Dockerfile",
            )),
            ycsb_runner_context=str(_get(
                "ycsb_runner_context",
                "./benchmarks/implementations/docker/ycsb_runner",
            )),
            ycsb_base_image=str(_get("ycsb_base_image", "eclipse-temurin:11-jre-jammy")),
            ycsb_release_url=str(_get(
                "ycsb_release_url",
                (
                    "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
                    "ycsb-redis-binding-0.17.0.tar.gz"
                ),
            )),
            ycsb_release_fallback_url=str(_get(
                "ycsb_release_fallback_url",
                (
                    "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
                    "ycsb-0.17.0.tar.gz"
                ),
            )),
            ycsb_datatype=str(_get("ycsb_datatype", "string")),
            ycsb_workloads=ycsb_wl,
            memtier_docker_image=str(_get("memtier_docker_image", "redislabs/memtier_benchmark:2.1.0")),
            memtier_scenarios=mt_scen,
        )

    def _select_suites(self, config: RedisBenchConfig, tier: str) -> List[str]:
        """Return the list of suite names to run for the given tier."""
        if config.suites:
            return list(dict.fromkeys(config.suites))

        tier_key = (tier or "").strip().lower()
        if tier_key in {"l0", "t0", "tier0"}:
            return ["tcl"]
        if tier_key in {"l1", "t1", "tier1"}:
            return ["tcl", "redis_benchmark"]
        if tier_key in {"l2", "t2", "tier2"}:
            return ["tcl", "redis_benchmark"]
        if tier_key in {"l3", "t3", "tier3"}:
            return ["tcl"]
        if tier_key in {"l4", "t4", "tier4"}:
            return ["tcl", "redis_benchmark"]
        if tier_key in {"l5", "t5", "tier5"}:
            return ["ycsb"]
        if tier_key in {"l6", "t6", "tier6"}:
            return ["tcl", "ycsb", "memtier"]
        # Default: tcl only
        return ["tcl"]

    # ------------------------------------------------------------------
    # Score calculation
    # ------------------------------------------------------------------

    def _calculate_score(self, workload_results: Dict[str, str]) -> float:
        if not workload_results:
            return 0.0
        passed = sum(1 for v in workload_results.values() if v == "PASS")
        return passed / len(workload_results)

    # ------------------------------------------------------------------
    # Suite helpers
    # ------------------------------------------------------------------

    def _redis_benchmark_tests_for_tier(
        self, config: RedisBenchConfig, tier: str
    ) -> List[Tuple[str, str]]:
        """Return redis-benchmark test definitions for the given tier."""
        if config.redis_benchmark_tests:
            tests: List[Tuple[str, str]] = []
            for raw_name in config.redis_benchmark_tests:
                name = str(raw_name).strip()
                if not name:
                    continue
                alias = REDIS_BENCHMARK_CONFIG_ALIASES.get(name)
                if alias is not None:
                    tests.append(alias)
                else:
                    tests.append((f"redis_benchmark:{name}", name))
            return tests
        tier_key = (tier or "").strip().lower()
        if tier_key in {"l1", "t1", "tier1"}:
            return list(REDIS_BENCHMARK_TESTS_L1)
        if tier_key in {"l4", "t4", "tier4"}:
            return list(REDIS_BENCHMARK_TESTS_L4)
        # L2 and default
        return list(REDIS_BENCHMARK_TESTS_L2)

    def _ycsb_workloads(self, config: RedisBenchConfig) -> List[Tuple[str, str]]:
        if config.ycsb_workloads:
            return [(f"ycsb:{w}", w) for w in config.ycsb_workloads]
        return list(YCSB_WORKLOADS)

    def _memtier_scenarios(self, config: RedisBenchConfig) -> List[Tuple[str, str]]:
        if config.memtier_scenarios:
            result = []
            for s in config.memtier_scenarios:
                for wid, args in MEMTIER_SCENARIOS:
                    if s == wid.split(":")[-1]:
                        result.append((wid, args))
                        break
                else:
                    result.append((f"memtier:{s}", ""))
            return result
        return list(MEMTIER_SCENARIOS)

    # ------------------------------------------------------------------
    # TCL suite
    # ------------------------------------------------------------------

    def _tcl_workload_count(self, config: RedisBenchConfig) -> int:
        """Count TCL workloads from ruleset file."""
        cases = self._load_tcl_ruleset(config)
        return max(len(cases), 1)

    def _tcl_workload_ids(self, config: RedisBenchConfig) -> List[str]:
        """Return TCL workload IDs from ruleset file."""
        cases = self._load_tcl_ruleset(config)
        return [f"tcl:{case}" for case in cases]

    def _load_tcl_ruleset(self, config: RedisBenchConfig) -> List[str]:
        """Load TCL test case list from ruleset file."""
        ruleset_file = config.tcl_ruleset
        if not ruleset_file:
            return []

        ruleset_dir = Path(config.ruleset_dir)
        if not ruleset_dir.is_absolute() and not ruleset_dir.exists():
            ruleset_dir = PROJECT_ROOT / config.ruleset_dir
        ruleset_path = ruleset_dir / ruleset_file
        if not ruleset_path.exists() and ruleset_path != BENCHMARK_RULESET_DIR / ruleset_file:
            fallback_path = BENCHMARK_RULESET_DIR / ruleset_file
            if fallback_path.exists():
                ruleset_path = fallback_path
        if not ruleset_path.exists():
            logger.warning(f"TCL ruleset file not found: {ruleset_path}")
            return []

        cases = []
        try:
            for line in ruleset_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    cases.append(line)
        except Exception as e:
            logger.warning(f"Failed to read TCL ruleset: {e}")

        return cases

    def _run_tcl_suite(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        output_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run TCL test suite. Returns (workload_results, metrics)."""
        results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        cases = self._load_tcl_ruleset(config)
        if not cases:
            logger.warning("No TCL cases to run (empty ruleset)")
            return results, metrics

        for case_id in cases:
            remaining = deadline - time.time()
            if remaining <= 0:
                results[f"tcl:{case_id}"] = "TIMEOUT"
                metrics[f"tcl:{case_id}"] = {"error": "benchmark timeout exhausted before workload start"}
                continue

            wid = f"tcl:{case_id}"
            try:
                timeout = min(int(remaining), 60)
                metrics[wid] = run_redis_case(
                    case_id=case_id,
                    host=host,
                    port=port,
                    timeout_sec=timeout,
                    output_dir=output_dir,
                )
                results[wid] = "PASS"
            except TimeoutError:
                results[wid] = "TIMEOUT"
                metrics[wid] = {"error": "workload timed out"}
            except RedisCaseFailure as e:
                results[wid] = "FAIL"
                metrics[wid] = {"error": str(e)}
            except Exception as e:
                results[wid] = "FAIL"
                metrics[wid] = {"error": str(e)}

        return results, metrics

    # ------------------------------------------------------------------
    # redis-benchmark suite
    # ------------------------------------------------------------------

    def _run_redis_benchmark_suite(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        output_dir: Path,
        deadline: float,
        tier: str,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run redis-benchmark suite. Returns (workload_results, metrics)."""
        results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        tests = self._redis_benchmark_tests_for_tier(config, tier)
        is_pipeline = tier.lower() in {"l4", "t4", "tier4"} if tier else False

        for wid, test_name in tests:
            remaining = deadline - time.time()
            if remaining <= 0:
                results[wid] = "TIMEOUT"
                metrics[wid] = {"error": "benchmark timeout exhausted before workload start"}
                continue

            timeout = min(int(remaining), 120)

            # Build redis-benchmark command
            cmd = self._build_redis_benchmark_cmd(
                host, port, config, test_name,
                pipeline=16 if is_pipeline and "pipeline" in wid else 0,
            )

            log_path = output_dir / f"{test_name}.log"
            try:
                result = self._run_shell(cmd, log_path, timeout)
                if result["returncode"] == 0:
                    parsed = self._parse_redis_benchmark_output(result["output"])
                    output_error, output_warnings = self._inspect_redis_benchmark_output(result["output"])
                    if output_error:
                        results[wid] = "FAIL"
                        metrics[wid] = {
                            **parsed,
                            "error": output_error,
                            "warnings": output_warnings,
                            "raw": result["output"][:500],
                        }
                    elif parsed and parsed.get("ops_per_sec", 0) > 0:
                        results[wid] = "PASS"
                        metrics[wid] = {
                            **parsed,
                            **({"warnings": output_warnings} if output_warnings else {}),
                        }
                    else:
                        results[wid] = "FAIL"
                        metrics[wid] = {"error": "zero throughput or parse failure", "raw": result["output"][:500]}
                elif result.get("error") == "timeout":
                    results[wid] = "TIMEOUT"
                    metrics[wid] = {"error": "workload timed out"}
                else:
                    results[wid] = "FAIL"
                    metrics[wid] = {"error": result.get("error") or result["output"][:500]}
            except Exception as e:
                results[wid] = "FAIL"
                metrics[wid] = {"error": str(e)}

        return results, metrics

    def _build_redis_benchmark_cmd(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        test_name: str,
        pipeline: int = 0,
    ) -> str:
        """Build a redis-benchmark docker run command."""
        pipeline_flag = f" -P {pipeline}" if pipeline > 0 else ""
        return (
            f"docker run --rm --network {config.network_mode} "
            f"{config.redis_benchmark_image} "
            f"redis-benchmark -h {host} -p {port} -t {test_name} "
            f"-n 1000 -c 10 --csv{pipeline_flag}"
        )

    def _parse_redis_benchmark_output(self, output: str) -> Dict[str, Any]:
        """Parse redis-benchmark --csv output."""
        parsed: Dict[str, Any] = {}
        total_ops = 0.0
        for match in REDIS_BENCH_CSV_RE.finditer(output):
            test = match.group("test")
            rps = float(match.group("rps"))
            parsed[f"test_{test}_rps"] = rps
            parsed[f"test_{test}_avg_latency_ms"] = float(match.group("avg"))
            parsed[f"test_{test}_p99_latency_ms"] = float(match.group("p99"))
            total_ops += rps
        if total_ops > 0:
            parsed["ops_per_sec"] = total_ops
        return parsed

    def _inspect_redis_benchmark_output(self, output: str) -> Tuple[Optional[str], List[str]]:
        """Classify non-CSV diagnostics from redis-benchmark output."""
        unexpected_lines: List[str] = []
        warning_lines: List[str] = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line == REDIS_BENCH_CSV_HEADER or REDIS_BENCH_CSV_RE.fullmatch(line):
                continue
            if line.startswith("WARNING:"):
                warning_lines.append(line)
            else:
                unexpected_lines.append(line)

        if unexpected_lines:
            return f"unexpected redis-benchmark output: {unexpected_lines[0]}", warning_lines
        return None, warning_lines

    # ------------------------------------------------------------------
    # YCSB suite
    # ------------------------------------------------------------------

    def _run_ycsb_suite(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        output_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run YCSB suite. Returns (workload_results, metrics)."""
        results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        workloads = self._ycsb_workloads(config)

        for wid, workload_name in workloads:
            remaining = deadline - time.time()
            if remaining <= 0:
                results[wid] = "TIMEOUT"
                metrics[wid] = {"error": "benchmark timeout exhausted before workload start"}
                continue

            timeout = min(int(remaining), 300)

            # Load phase
            load_cmd = self._build_ycsb_cmd(
                host, port, config, workload_name, phase="load",
            )
            load_log = output_dir / f"{workload_name}_load.log"
            load_result = self._run_shell(load_cmd, load_log, timeout)
            load_error, load_warnings = self._inspect_ycsb_output(load_result["output"])
            if load_result["returncode"] != 0:
                results[wid] = "FAIL"
                metrics[wid] = {"error": f"YCSB load phase failed: {load_result.get('error') or load_result['output'][:500]}"}
                continue
            if load_error:
                results[wid] = "FAIL"
                metrics[wid] = {
                    "error": f"YCSB load phase error: {load_error}",
                    **({"warnings": [f"load: {warning}" for warning in load_warnings]} if load_warnings else {}),
                    "raw": load_result["output"][:500],
                }
                continue

            # Run phase
            run_cmd = self._build_ycsb_cmd(
                host, port, config, workload_name, phase="run",
            )
            run_log = output_dir / f"{workload_name}_run.log"
            run_result = self._run_shell(run_cmd, run_log, timeout)

            if run_result["returncode"] == 0:
                ycsb_metrics = self._parse_ycsb_output(run_result["output"])
                run_error, run_warnings = self._inspect_ycsb_output(run_result["output"])
                warnings = [f"load: {warning}" for warning in load_warnings]
                warnings.extend(f"run: {warning}" for warning in run_warnings)
                error_count = ycsb_metrics.get("error_count", 0)
                throughput = ycsb_metrics.get("throughput_ops_sec", 0)
                if run_error:
                    results[wid] = "FAIL"
                    metrics[wid] = {
                        **ycsb_metrics,
                        "error": f"YCSB run phase error: {run_error}",
                        **({"warnings": warnings} if warnings else {}),
                        "raw": run_result["output"][:500],
                    }
                elif error_count > 0:
                    results[wid] = "FAIL"
                    metrics[wid] = {
                        **ycsb_metrics,
                        "error": f"YCSB reported {error_count} errors",
                        **({"warnings": warnings} if warnings else {}),
                    }
                elif throughput > 0:
                    results[wid] = "PASS"
                    metrics[wid] = {
                        **ycsb_metrics,
                        **({"warnings": warnings} if warnings else {}),
                    }
                else:
                    results[wid] = "FAIL"
                    metrics[wid] = {
                        **ycsb_metrics,
                        "error": "zero throughput",
                        **({"warnings": warnings} if warnings else {}),
                    }
            elif run_result.get("error") == "timeout":
                results[wid] = "TIMEOUT"
                metrics[wid] = {"error": "workload timed out"}
            else:
                results[wid] = "FAIL"
                metrics[wid] = {"error": run_result.get("error") or run_result["output"][:500]}

        return results, metrics

    def _build_ycsb_cmd(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        workload: str,
        phase: str = "run",
    ) -> str:
        """Build a YCSB docker run command using the local runner image."""
        return (
            f"docker run --rm --network {shlex.quote(config.network_mode)} "
            f"{shlex.quote(config.ycsb_runner_image)} "
            f"{phase} redis -s "
            f"-P {shlex.quote(f'workloads/workload{workload}')} "
            f"-p {shlex.quote(f'redis.host={host}')} "
            f"-p {shlex.quote(f'redis.port={port}')} "
            f"-p {shlex.quote(f'redis.datatype={config.ycsb_datatype}')} "
            f"-p recordcount=1000 -p operationcount=1000"
        )

    def _parse_ycsb_output(self, output: str) -> Dict[str, Any]:
        """Parse YCSB output for throughput and error counts."""
        metrics: Dict[str, Any] = {}
        tp_match = YCSB_THROUGHPUT_RE.search(output)
        if tp_match:
            metrics["throughput_ops_sec"] = float(tp_match.group(1))

        error_count = 0
        for m in YCSB_ERROR_RE.finditer(output):
            error_count += int(m.group(1))
        metrics["error_count"] = error_count

        return metrics

    def _inspect_ycsb_output(self, output: str) -> Tuple[Optional[str], List[str]]:
        """Classify YCSB diagnostics without treating warnings as failures."""
        warning_lines: List[str] = []
        error_lines: List[str] = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if YCSB_WARNING_LINE_RE.search(line):
                warning_lines.append(line)
            elif YCSB_ERROR_LINE_RE.search(line):
                error_lines.append(line)

        if error_lines:
            return f"unexpected YCSB output: {error_lines[0]}", warning_lines
        return None, warning_lines

    # ------------------------------------------------------------------
    # memtier suite
    # ------------------------------------------------------------------

    def _run_memtier_suite(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        output_dir: Path,
        deadline: float,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """Run memtier suite. Returns (workload_results, metrics)."""
        results: Dict[str, str] = {}
        metrics: Dict[str, Any] = {}

        scenarios = self._memtier_scenarios(config)

        for wid, extra_args in scenarios:
            remaining = deadline - time.time()
            if remaining <= 0:
                results[wid] = "TIMEOUT"
                metrics[wid] = {"error": "benchmark timeout exhausted before workload start"}
                continue

            timeout = min(int(remaining), 120)
            scenario_name = wid.split(":")[-1]

            cmd = self._build_memtier_cmd(host, port, config, extra_args)
            log_path = output_dir / f"{scenario_name}.log"

            try:
                result = self._run_shell(cmd, log_path, timeout)
                if result["returncode"] == 0:
                    mt_metrics = self._parse_memtier_output(result["output"])
                    output_error, output_warnings = self._inspect_memtier_output(result["output"])
                    ops = mt_metrics.get("total_ops_sec", 0)
                    if output_error:
                        results[wid] = "FAIL"
                        metrics[wid] = {
                            **mt_metrics,
                            "error": output_error,
                            "warnings": output_warnings,
                            "raw": result["output"][:500],
                        }
                    elif ops > 0:
                        results[wid] = "PASS"
                        metrics[wid] = {
                            **mt_metrics,
                            **({"warnings": output_warnings} if output_warnings else {}),
                        }
                    else:
                        results[wid] = "FAIL"
                        metrics[wid] = {
                            **mt_metrics,
                            "error": "zero throughput",
                            **({"warnings": output_warnings} if output_warnings else {}),
                        }
                elif result.get("error") == "timeout":
                    results[wid] = "TIMEOUT"
                    metrics[wid] = {"error": "workload timed out"}
                else:
                    results[wid] = "FAIL"
                    metrics[wid] = {"error": result.get("error") or result["output"][:500]}
            except Exception as e:
                results[wid] = "FAIL"
                metrics[wid] = {"error": str(e)}

        return results, metrics

    def _build_memtier_cmd(
        self,
        host: str,
        port: int,
        config: RedisBenchConfig,
        extra_args: str,
    ) -> str:
        """Build a memtier_benchmark docker run command."""
        return (
            f"docker run --rm --network {config.network_mode} "
            f"{config.memtier_docker_image} "
            f"memtier_benchmark -s {host} -p {port} "
            f"--protocol=redis {extra_args}"
        )

    def _parse_memtier_output(self, output: str) -> Dict[str, Any]:
        """Parse memtier_benchmark output."""
        metrics: Dict[str, Any] = {}
        match = MEMTIER_TOTALS_RE.search(output)
        if match:
            metrics["total_ops_sec"] = float(match.group("ops"))
            metrics["avg_latency_ms"] = float(match.group("avg_latency"))
            metrics["p99_latency_ms"] = float(match.group("p99_latency"))

        if metrics.get("total_ops_sec", 0) <= 0:
            progress_match = None
            for progress_match in MEMTIER_PROGRESS_RE.finditer(output):
                pass
            if progress_match:
                metrics["total_ops_sec"] = float(progress_match.group("ops"))
                metrics.setdefault("avg_latency_ms", float(progress_match.group("avg_latency")))
        return metrics

    def _inspect_memtier_output(self, output: str) -> Tuple[Optional[str], List[str]]:
        """Classify memtier diagnostics without treating warnings as failures."""
        warning_lines: List[str] = []
        error_lines: List[str] = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if MEMTIER_WARNING_LINE_RE.search(line):
                warning_lines.append(line)
            elif MEMTIER_ERROR_LINE_RE.search(line):
                error_lines.append(line)

        if error_lines:
            return f"unexpected memtier output: {error_lines[0]}", warning_lines
        return None, warning_lines

    # ------------------------------------------------------------------
    # Shell execution helper
    # ------------------------------------------------------------------

    def _run_shell(
        self,
        cmd: str,
        log_path: Path,
        timeout_sec: int,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run a shell command with timeout. Returns dict with returncode, output, error."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                env=env or os.environ,
                cwd=cwd,
            )
            output = result.stdout + result.stderr
            try:
                log_path.write_text(output)
            except Exception:
                pass
            return {
                "returncode": result.returncode,
                "output": output,
                "error": None if result.returncode == 0 else output[:500],
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -9,
                "output": "[TIMEOUT]\n",
                "error": "timeout",
            }
        except Exception as e:
            return {
                "returncode": -1,
                "output": str(e),
                "error": str(e),
            }

    @staticmethod
    def _remaining_timeout(deadline: float) -> int:
        """Return whole-second timeout budget remaining until the shared deadline."""
        remaining = deadline - time.time()
        if remaining <= 0:
            return 0
        return max(1, int(remaining))


# Register the benchmark
from ..registry import register_benchmark
register_benchmark("redis_bench", RedisBenchRunner)
