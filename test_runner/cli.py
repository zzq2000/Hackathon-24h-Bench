"""
CLI entrypoint for the modular test runner.

This module powers:
  - python -m test_runner
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import signal
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from sut import create_sut, load_config
from test_runner import TestOrchestrator
from test_runner.preflight import run_dependency_preflight

logger = logging.getLogger(__name__)


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = dict(base)
    for key, value in (override or {}).items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _ensure_run_log_dir(log_dir: Path, run_id: str) -> Path:
    run_dir = log_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    latest = log_dir / "latest"
    try:
        if latest.is_symlink() or latest.exists():
            latest.unlink()
        latest.symlink_to(Path("runs") / run_id)
    except OSError:
        # Symlink failure is non-fatal (e.g., filesystem restrictions)
        pass

    return run_dir


def _load_latest_snapshot_commit(log_dir: Optional[Path], run_id: str) -> Optional[Tuple[str, int]]:
    if not log_dir:
        return None
    snapshot_path = log_dir / "runs" / run_id / "latest_snapshot.json"
    if not snapshot_path.exists():
        return None
    try:
        raw = json.loads(snapshot_path.read_text(encoding="utf-8"))
        commit = (raw.get("commit") or "").strip()
        iteration = int(raw.get("iteration", 0))
        if not commit:
            return None
        return commit, iteration
    except Exception:
        return None


def _is_controller_done(log_dir: Optional[Path], run_id: str, since: float = 0.0) -> bool:
    """Check if the controller has written a done marker after *since* (epoch).

    Comparing against *since* prevents stale markers from a previous controller
    run from triggering an immediate exit (e.g. when using ``--runner-only``).
    """
    if not log_dir:
        return False
    marker_path = log_dir / "runs" / run_id / "controller_done.json"
    if not marker_path.exists():
        return False
    # Only honour markers created after the test runner started
    try:
        return marker_path.stat().st_mtime >= since
    except OSError:
        return False


def _scan_max_index(parent_dir: Path, prefix: str) -> int:
    """Scan a directory and return max numeric suffix for names like '<prefix><number>'."""
    if not parent_dir.exists():
        return 0

    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    max_index = 0
    for entry in parent_dir.iterdir():
        if not entry.is_dir():
            continue
        match = pattern.match(entry.name)
        if not match:
            continue
        try:
            max_index = max(max_index, int(match.group(1)))
        except ValueError:
            continue
    return max_index


def _find_resume_test_index(run_id: str, test_base_dir: Path, output_base_dir: Path) -> int:
    """
    Find the last used test index for this run.

    Uses both test instance and output directories and returns the larger value.
    """
    test_parent = test_base_dir / run_id
    output_parent = output_base_dir / run_id
    max_test = _scan_max_index(test_parent, "test_instance_")
    max_output = _scan_max_index(output_parent, "output_")
    return max(max_test, max_output)


def _resolve_runtime_dir(value: str, work_dir: Path, default_name: str) -> Path:
    path = Path(value).expanduser() if value else Path(default_name)
    if not path.is_absolute():
        path = work_dir / path
    return path.resolve()


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Modular test runner")
    parser.add_argument(
        "--system-type",
        default=os.environ.get("SYSTEM_TYPE", "database"),
        help="System type (database, message_queue)",
    )
    parser.add_argument(
        "--sut-dir",
        default="",
        help="SUT working directory (preferred; e.g., ./workspace/database/database_gpt or ./message_queue_gpt)",
    )
    parser.add_argument(
        "--config-file",
        default="",
        help="Path to main config file (default: ./config/global.yaml)",
    )
    parser.add_argument(
        "--bench-file",
        default="",
        help="Optional benchmark override config file (default: none)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help="Submit interval between test cycles in seconds (start-to-start, default: 900)",
    )
    parser.add_argument(
        "--first-delay",
        type=int,
        default=None,
        help=(
            "Delay before first test in seconds. "
            "When AGENT_START_EPOCH is set, this delay is counted from controller start "
            "(default from env FIRST_TEST_DELAY_SEC or 3600)."
        ),
    )
    parser.add_argument(
        "--benchmark-timeout",
        type=int,
        default=None,
        help="Per-benchmark timeout seconds (default: from config/global.yaml, currently 900)",
    )
    parser.add_argument(
        "--log-dir",
        default=os.environ.get("LOG_DIR", ""),
        help="Logs root directory (default: $LOG_DIR)",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Output base directory (default: ./output or config/global.yaml benchmark.output_dir)",
    )
    parser.add_argument(
        "--test-base-dir",
        default="",
        help="Test instances base directory (default: ./test_instances or config/global.yaml test_runner.test_base_dir)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run exactly one test cycle",
    )
    parser.add_argument(
        "--tiers",
        default="",
        help="Comma-separated tiers to run (default: system-specific tiers if available)",
    )
    parser.add_argument(
        "--benchmarks",
        default="",
        help="Comma-separated benchmarks to run (default: enabled benchmarks in config/system.<type>.yaml)",
    )
    parser.add_argument(
        "--tier-mode",
        choices=("ladder", "full"),
        default=None,
        help=(
            "Tier execution/report mode: "
            "'ladder' stops after the first failed tier and only reports that tier; "
            "'full' runs all tiers and reports each tier"
        ),
    )
    parser.add_argument(
        "--no-console-log",
        action="store_true",
        help="Disable console logging; keep file logging only when --log-dir is set",
    )
    parser.set_defaults(run_all_tiers=None)
    parser.add_argument(
        "--run-all-tiers",
        dest="run_all_tiers",
        action="store_true",
        help="Run all tiers even if earlier tiers fail (default behavior)",
    )
    parser.add_argument(
        "--stop-on-tier-failure",
        dest="run_all_tiers",
        action="store_false",
        help="Skip remaining tiers after the first failed tier",
    )
    return parser.parse_args(argv)


def _env_flag(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip().lower()
    return value not in {"0", "false", "no", "off", ""}


def _setup_logging(run_dir: Optional[Path], *, console_log: bool) -> None:
    handlers: List[logging.Handler] = []
    if console_log:
        handlers.append(logging.StreamHandler(sys.stdout))
    if run_dir:
        handlers.append(logging.FileHandler(run_dir / "test_runner.log"))
    if not handlers:
        handlers.append(logging.NullHandler())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def _sanitize_model(model: str) -> str:
    return model.replace("/", "-").replace("\\", "-").replace(":", "-").replace(" ", "_")


def _resolve_agent_name() -> str:
    return (os.environ.get("AGENT_NAME") or os.environ.get("CODE_AGENT") or "agent").strip() or "agent"


def _resolve_agent_type(agent_name: Optional[str] = None) -> str:
    # Use CODE_AGENT (agent type) for selecting env vars like CODEX_MODEL / CLAUDE_MODEL.
    agent_type = (os.environ.get("CODE_AGENT") or "").strip()
    if agent_type:
        return agent_type
    return (agent_name or "agent").strip() or "agent"


def _resolve_agent_model(agent_type: str) -> str:
    agent_upper = (agent_type or "").strip().upper()
    model = (
        os.environ.get("CODE_AGENT_MODEL")
        or (os.environ.get(f"{agent_upper}_MODEL") if agent_upper else None)
        or "unknown"
    )
    return _sanitize_model(model)


def _default_run_id(
    *,
    system_type: Optional[str] = None,
    agent_name: Optional[str] = None,
    agent_type: Optional[str] = None,
) -> str:
    resolved_system_type = (system_type or os.environ.get("SYSTEM_TYPE") or "database").strip() or "database"
    resolved_agent_name = (agent_name or _resolve_agent_name()).strip() or "agent"
    resolved_agent_type = (agent_type or _resolve_agent_type(resolved_agent_name)).strip() or "agent"
    model = _resolve_agent_model(resolved_agent_type)
    return f"{resolved_system_type}_{resolved_agent_name}_{model}_{datetime.now():%Y%m%d_%H%M%S}"


def _select_tiers(cfg, cli_tiers: str) -> List[str]:
    if cli_tiers.strip():
        return [t.strip() for t in cli_tiers.split(",") if t.strip()]

    # Use all tiers from system config; fall back to DEFAULT_TIERS only when
    # the system config defines none.
    return cfg.get_tiers() or TestOrchestrator.DEFAULT_TIERS


def _select_benchmarks(cfg, cli_benchmarks: str) -> List[str]:
    if cli_benchmarks.strip():
        return [b.strip() for b in cli_benchmarks.split(",") if b.strip()]
    return cfg.get_benchmarks()


def _resolve_run_all_tiers(cli_value: Optional[bool], systems_cfg: Dict[str, Any]) -> bool:
    if cli_value is not None:
        return bool(cli_value)

    env_value = os.environ.get("RUN_ALL_TIERS")
    if env_value is not None:
        return _env_flag("RUN_ALL_TIERS", True)

    runner_cfg = (systems_cfg.get("test_runner", {}) or {})
    if not isinstance(runner_cfg, dict):
        return True
    if "run_all_tiers" in runner_cfg:
        return bool(runner_cfg.get("run_all_tiers"))
    return True


def _normalize_tier_mode(value: Any) -> Optional[str]:
    if value is None:
        return None

    normalized = str(value).strip().lower()
    if not normalized:
        return None

    aliases = {
        "ladder": "ladder",
        "step": "ladder",
        "staged": "ladder",
        "sequential": "ladder",
        "full": "full",
        "all": "full",
        "diagnostic": "full",
    }
    return aliases.get(normalized)


def _resolve_tier_mode(
    cli_value: Optional[str],
    cli_run_all_tiers: Optional[bool],
    systems_cfg: Dict[str, Any],
) -> str:
    cli_mode = _normalize_tier_mode(cli_value)
    if cli_mode:
        return cli_mode

    env_mode = _normalize_tier_mode(os.environ.get("TIER_MODE"))
    if env_mode:
        return env_mode

    runner_cfg = (systems_cfg.get("test_runner", {}) or {})
    if isinstance(runner_cfg, dict):
        cfg_mode = _normalize_tier_mode(runner_cfg.get("tier_mode"))
        if cfg_mode:
            return cfg_mode

    run_all_tiers = _resolve_run_all_tiers(cli_run_all_tiers, systems_cfg)
    return "full" if run_all_tiers else "ladder"


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)

    system_type = (args.system_type or "database").strip()
    os.environ["SYSTEM_TYPE"] = system_type
    config_file = Path(args.config_file).expanduser().resolve() if args.config_file else None

    bench_file: Optional[Path] = Path(args.bench_file).expanduser().resolve() if args.bench_file else None

    agent_name = _resolve_agent_name()
    agent_type = _resolve_agent_type(agent_name)
    agent_model = _resolve_agent_model(agent_type)

    run_id = (os.environ.get("AGENT_RUN_ID") or "").strip() or _default_run_id(
        system_type=system_type,
        agent_name=agent_name,
        agent_type=agent_type,
    )
    os.environ["AGENT_RUN_ID"] = run_id

    log_dir = Path(args.log_dir).expanduser().resolve() if args.log_dir else None
    run_dir = _ensure_run_log_dir(log_dir, run_id) if log_dir else None
    console_log = _env_flag("TEST_RUNNER_CONSOLE_LOG", True) and (not args.no_console_log)
    _setup_logging(run_dir, console_log=console_log)

    # Load hierarchical config: config/system.<type>.yaml -> config/global.yaml -> optional benchmark override
    cfg = load_config(system_type, config_file=config_file, bench_file=bench_file)
    tiers = _select_tiers(cfg, args.tiers)
    benchmarks = _select_benchmarks(cfg, args.benchmarks)
    if not benchmarks:
        logger.error(f"No benchmarks enabled for system_type={system_type}")
        return 1

    config_dict = cfg.to_dict()
    systems_cfg = config_dict.get("config", {}) or {}
    bench_cfg = config_dict.get("bench_config", {}) or {}
    tier_mode = _resolve_tier_mode(args.tier_mode, args.run_all_tiers, systems_cfg)
    run_all_tiers = tier_mode == "full"

    sut_dir = (args.sut_dir or "").strip()
    if sut_dir:
        sut_dir_path = Path(sut_dir).expanduser().resolve()
    else:
        sut_dir_path = cfg.get_target_dir().expanduser().resolve()
        # When target_dir points at the workspace base (./workspace/{system_type}),
        # place this run under ./workspace/{system_type}/{run_id}.
        if sut_dir_path.name == system_type and sut_dir_path.parent.name == "workspace":
            sut_dir_path = (sut_dir_path / run_id).resolve()

    interval = (
        args.interval
        if args.interval is not None
        else int(os.environ.get("TEST_INTERVAL") or (systems_cfg.get("test_runner", {}) or {}).get("test_interval", 900))
    )
    first_delay_sec = (
        args.first_delay
        if args.first_delay is not None
        else int(os.environ.get("FIRST_TEST_DELAY_SEC", "3600"))
    )
    benchmark_timeout = (
        args.benchmark_timeout
        if args.benchmark_timeout is not None
        else int(os.environ.get("BENCHMARK_TIMEOUT") or (systems_cfg.get("test_runner", {}) or {}).get("benchmark_timeout", 600))
    )
    logger.info("tier_mode=%s", tier_mode)
    logger.info("run_all_tiers=%s", run_all_tiers)

    docker_cfg = _deep_merge(cfg.get_docker_config(), bench_cfg.get("docker", {}) or {})
    db_cfg = _deep_merge(systems_cfg.get(system_type, {}) or {}, bench_cfg.get("db", {}) or {})

    tier_configs: Dict[str, Dict[str, Any]] = {}
    tier_timeout_multipliers: Dict[str, float] = {}
    for tier in tiers:
        tier_configs[tier] = {}
        tier_cfg = cfg.get_tier_config(tier)
        if isinstance(tier_cfg, dict):
            try:
                tier_timeout_multipliers[tier] = float(tier_cfg.get("timeout_multiplier", 1.0))
            except Exception:
                tier_timeout_multipliers[tier] = 1.0
        else:
            tier_timeout_multipliers[tier] = 1.0

        for bench in benchmarks:
            bench_config = cfg.get_benchmark_config(bench, tier=tier)
            # Flatten common config into the shapes expected by built-in benchmarks.
            if system_type == "database":
                if isinstance(db_cfg, dict):
                    bench_config.setdefault("db_user", db_cfg.get("user", "root"))
                    bench_config.setdefault("db_password", db_cfg.get("password", "root"))
                if isinstance(docker_cfg, dict):
                    bench_config.setdefault("network_mode", docker_cfg.get("network_mode", "host"))
                    if bench == "sysbench":
                        bench_config.setdefault("docker_image", docker_cfg.get("sysbench_image"))
                    elif bench in {"tpcc", "tpch"}:
                        bench_config.setdefault("docker_image", docker_cfg.get("hammerdb_image"))
            tier_configs[tier][bench] = bench_config

    sut_section = systems_cfg.get(system_type, {})
    if not isinstance(sut_section, dict):
        sut_section = {}

    work_dir_path = Path(__file__).resolve().parent.parent
    try:
        run_dependency_preflight(
            system_type=system_type,
            tiers=tiers,
            benchmarks=benchmarks,
            tier_configs=tier_configs,
            docker_cfg=docker_cfg if isinstance(docker_cfg, dict) else {},
            work_dir=work_dir_path,
        )
    except Exception as e:
        logger.error("Dependency preflight failed: %s", e)
        return 1

    output_dir = (args.output_dir or "").strip()
    if not output_dir:
        output_dir = str((systems_cfg.get("benchmark", {}) or {}).get("output_dir", "")).strip()

    test_base_dir = (args.test_base_dir or "").strip()
    if not test_base_dir:
        test_base_dir = str((systems_cfg.get("test_runner", {}) or {}).get("test_base_dir", "")).strip()

    sut = create_sut(system_type, sut_dir_path, sut_section)
    orchestrator_config: Dict[str, Any] = {
        "work_dir": str(work_dir_path),
        "tiers": tiers,
        "tier_configs": tier_configs,
        "tier_timeout_multipliers": tier_timeout_multipliers,
        "agent": agent_name,
        "agent_type": agent_type,
        "agent_model": agent_model,
        "tier_mode": tier_mode,
        "run_all_tiers": run_all_tiers,
    }
    if test_base_dir:
        orchestrator_config["test_base_dir"] = test_base_dir
    if output_dir:
        orchestrator_config["output_base_dir"] = output_dir

    orchestrator = TestOrchestrator(
        sut,
        benchmarks=benchmarks,
        config=orchestrator_config,
    )

    resolved_test_base_dir = _resolve_runtime_dir(test_base_dir, work_dir_path, "test_instances")
    resolved_output_base_dir = _resolve_runtime_dir(output_dir, work_dir_path, "output")

    stop_event = {"stop": False}

    def _handle_stop(sig, frame) -> None:  # noqa: ARG001
        logger.info(f"Received signal {sig}, stopping...")
        stop_event["stop"] = True

    signal.signal(signal.SIGINT, _handle_stop)
    signal.signal(signal.SIGTERM, _handle_stop)

    test_index = _find_resume_test_index(
        run_id=run_id,
        test_base_dir=resolved_test_base_dir,
        output_base_dir=resolved_output_base_dir,
    )
    if test_index > 0:
        logger.info(
            "Detected existing test index up to %s, next test will start from %s",
            test_index,
            test_index + 1,
        )
    first_run_not_before: Optional[float] = None
    agent_start_epoch_raw = (os.environ.get("AGENT_START_EPOCH") or "").strip()
    if agent_start_epoch_raw:
        try:
            agent_start_epoch = float(agent_start_epoch_raw)
            if first_delay_sec > 0:
                first_run_not_before = agent_start_epoch + first_delay_sec
                logger.info(
                    "First test will run no earlier than %s (agent start + %ss)",
                    datetime.fromtimestamp(first_run_not_before).isoformat(timespec="seconds"),
                    first_delay_sec,
                )
        except ValueError:
            logger.warning("Invalid AGENT_START_EPOCH=%r, skipping first-test delay", agent_start_epoch_raw)

    snapshot_deadline: Optional[float] = None
    last_first_delay_log_sec: Optional[int] = None
    runner_start_epoch = time.time()
    next_cycle_not_before: Optional[float] = None
    active_cycle_threads: Dict[int, threading.Thread] = {}
    active_cycle_lock = threading.Lock()

    def _active_cycle_count() -> int:
        with active_cycle_lock:
            return len(active_cycle_threads)

    def _join_active_cycle_threads() -> None:
        while True:
            with active_cycle_lock:
                threads = list(active_cycle_threads.values())
            if not threads:
                return
            for thread in threads:
                thread.join(timeout=1)

    def _run_cycle_async(
        cycle_test_index: int,
        cycle_snapshot_commit: Optional[str],
        cycle_snapshot_time: str,
    ) -> None:
        try:
            orchestrator.run_cycle(
                run_id=run_id,
                test_index=cycle_test_index,
                benchmark_timeout_sec=benchmark_timeout,
                snapshot_commit=cycle_snapshot_commit,
                snapshot_time=cycle_snapshot_time,
            )
        except Exception as e:
            logger.error("Async test cycle %s failed: %s", cycle_test_index, e, exc_info=True)
        finally:
            with active_cycle_lock:
                active_cycle_threads.pop(cycle_test_index, None)

    def _submit_cycle_async(
        cycle_test_index: int,
        cycle_snapshot_commit: Optional[str],
        cycle_snapshot_time: str,
    ) -> None:
        thread = threading.Thread(
            target=_run_cycle_async,
            args=(cycle_test_index, cycle_snapshot_commit, cycle_snapshot_time),
            name=f"test-cycle-{run_id}-{cycle_test_index}",
        )
        with active_cycle_lock:
            active_cycle_threads[cycle_test_index] = thread
        thread.start()
        logger.info(
            "Submitted test cycle %s (active cycles: %s)",
            cycle_test_index,
            _active_cycle_count(),
        )

    if log_dir and args.once:
        snapshot_deadline = time.time() + int(os.environ.get("WAIT_SNAPSHOT_SEC", "600"))
    controller_done_logged = False
    try:
        while not stop_event["stop"]:
            if next_cycle_not_before is not None:
                now = time.time()
                if now < next_cycle_not_before:
                    time.sleep(min(1.0, next_cycle_not_before - now))
                    continue

            # Check if the controller has finished (e.g. max iterations reached)
            if _is_controller_done(log_dir, run_id, since=runner_start_epoch):
                if not controller_done_logged:
                    logger.info("Controller done marker detected, will run final test and exit.")
                    controller_done_logged = True
                if not args.once and _active_cycle_count() > 0:
                    logger.info("Waiting for %s active cycles before final test...", _active_cycle_count())
                    _join_active_cycle_threads()
                # Run one final test cycle on the latest snapshot, then exit
                snapshot_time = datetime.now().isoformat(timespec="seconds")
                snapshot = _load_latest_snapshot_commit(log_dir, run_id)
                if snapshot is not None:
                    test_index += 1
                    snapshot_commit = snapshot[0] if snapshot else None
                    if snapshot_commit:
                        logger.info(f"Final test using snapshot commit: {snapshot_commit[:12]}")
                    orchestrator.run_cycle(
                        run_id=run_id,
                        test_index=test_index,
                        benchmark_timeout_sec=benchmark_timeout,
                        snapshot_commit=snapshot_commit,
                        snapshot_time=snapshot_time,
                    )
                logger.info("Controller finished and final test completed, stopping test runner.")
                break

            if test_index == 0 and first_run_not_before is not None:
                now = time.time()
                if now < first_run_not_before:
                    remaining = int(first_run_not_before - now)
                    remaining_bucket = remaining // 60
                    if last_first_delay_log_sec is None or remaining_bucket != (last_first_delay_log_sec // 60):
                        logger.info("Waiting %ss before first test (aligned to controller start)...", remaining)
                        last_first_delay_log_sec = remaining
                    time.sleep(min(5, max(1, remaining)))
                    continue

            cycle_start_epoch = time.time()
            snapshot_time = datetime.now().isoformat(timespec="seconds")
            snapshot = _load_latest_snapshot_commit(log_dir, run_id)
            if log_dir and snapshot is None:
                if snapshot_deadline is not None and time.time() > snapshot_deadline:
                    logger.error("Timed out waiting for latest_snapshot.json from controller")
                    return 1
                logger.info("Waiting for controller snapshot (latest_snapshot.json)...")
                time.sleep(5)
                continue

            test_index += 1
            snapshot_commit = snapshot[0] if snapshot else None

            if snapshot_commit:
                logger.info(f"Using snapshot commit: {snapshot_commit[:12]}")

            if args.once:
                result = orchestrator.run_cycle(
                    run_id=run_id,
                    test_index=test_index,
                    benchmark_timeout_sec=benchmark_timeout,
                    snapshot_commit=snapshot_commit,
                    snapshot_time=snapshot_time,
                )
                return 0 if result.overall_status == "Accepted" else 1

            _submit_cycle_async(
                cycle_test_index=test_index,
                cycle_snapshot_commit=snapshot_commit,
                cycle_snapshot_time=snapshot_time,
            )

            # Align periodic scheduling to cycle start(submit) time.
            next_cycle_not_before = cycle_start_epoch + max(interval, 0)
    finally:
        if stop_event["stop"] and _active_cycle_count() > 0:
            logger.info("Stopping %s active cycles...", _active_cycle_count())
            orchestrator.cleanup_all()
        _join_active_cycle_threads()

    return 0
