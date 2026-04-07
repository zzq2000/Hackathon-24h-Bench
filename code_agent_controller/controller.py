"""
主控制器模块

提供命令行接口和主循环逻辑。
"""

import os
import sys
import time
import logging
import argparse
import json
import re
import subprocess
import tempfile
import fcntl
from contextlib import contextmanager
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from .utils import (
    WORK_DIR,
    load_env_file,
    setup_logging,
    ensure_directory,
    has_sut_files,
    get_env,
    LogManager,
)
from .registry import create_agent, get_available_agents, list_agents_info
from .loader import load_custom_agents
from .docker_runner import DockerAgentRunner, check_docker_available, DEFAULT_IMAGE_NAME
from sut import get_available_suts

try:
    import yaml
except Exception:  # pragma: no cover - 运行期可用性由 requirements 保证
    yaml = None

logger = logging.getLogger(__name__)
_ITER_FILE_RE = re.compile(r"^iter_(\d+)\.json$")
DEFAULT_WAIT_TIME_SECONDS = 60
DEFAULT_MAX_RETRIES = 3
DEFAULT_COMMAND_TIMEOUT_SECONDS = 300
DEFAULT_INIT_COMMAND_TIMEOUT_SECONDS = 10800   # 3 hours
DEFAULT_IMPROVE_COMMAND_TIMEOUT_SECONDS = 3600  # 1 hour
DEFAULT_COMPLETION_GRACE_SECONDS = 30
RATE_LIMIT_WAIT_TIME_SECONDS = 300
SNAPSHOT_REF = "refs/hackathon-24h-bench/snapshots/latest"
BASELINE_SNAPSHOT_REF_PREFIX = "refs/hackathon-24h-bench/baselines"

# 默认 SUT 工作目录（base workspace; actual run dir is ./workspace/{system_type}/{run_id}）
DEFAULT_SUT_DIR = WORK_DIR / "workspace" / "database"


def _sanitize_run_id_component(value: str) -> str:
    return value.replace("/", "_").replace("\\", "_").replace(":", "-").replace(" ", "_")


def _resolve_or_make_run_id(system_type: str, agent: str, model: Optional[str]) -> str:
    env_run_id = os.environ.get("AGENT_RUN_ID")
    if isinstance(env_run_id, str) and env_run_id.strip():
        return _sanitize_run_id_component(env_run_id.strip())

    if model:
        model_str = model
    else:
        agent_upper = agent.upper()
        model_str = (
            os.environ.get("CODE_AGENT_MODEL")
            or os.environ.get(f"{agent_upper}_MODEL")
            or "unknown"
        )

    model_str = _sanitize_run_id_component(model_str).replace("__", "_")
    return f"{system_type}_{agent}_{model_str}_{datetime.now():%Y%m%d_%H%M%S}"


def _is_workspace_base_dir(path: Path, system_type: str) -> bool:
    # Matches .../workspace/<system_type>
    return path.name == system_type and path.parent.name == "workspace"


def _is_rate_limit_error_from_result(result: Optional[object]) -> bool:
    """Best-effort 检测模型调用是否触发了 429 / rate limit。"""
    if result is None:
        return False

    stdout = str(getattr(result, "stdout", "") or "")
    stderr = str(getattr(result, "stderr", "") or "")
    text = f"{stdout}\n{stderr}".lower()
    return "429" in text or "rate limit" in text or "too many requests" in text


def _atomic_write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def _baseline_snapshot_ref(run_id: str) -> str:
    return f"{BASELINE_SNAPSHOT_REF_PREFIX}/{_sanitize_run_id_component(run_id)}"


def _is_git_repo(path: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def _ensure_git_repo(path: Path) -> bool:
    if _is_git_repo(path):
        return True
    try:
        result = subprocess.run(
            ["git", "init"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            logger.warning(f"git init 失败: {(result.stderr or result.stdout).strip()}")
            return False
        return True
    except Exception as e:
        logger.warning(f"初始化 git 仓库失败: {e}")
        return False


def _git_head_commit(path: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception:
        return None


def _git_has_changes(path: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return False
        return bool(result.stdout.strip())
    except Exception:
        return False


@contextmanager
def _git_repo_lock(path: Path, timeout_sec: float = 60.0):
    """
    Cross-process lock for git operations touching the same repository.
    """
    lock_path = path / ".hackathon-24h-bench.git.lock"
    fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR, 0o644)
    start = time.time()
    acquired = False
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
                break
            except BlockingIOError:
                if time.time() - start >= timeout_sec:
                    raise TimeoutError(f"Timed out waiting for git lock: {lock_path}")
                time.sleep(0.1)
        yield
    finally:
        try:
            if acquired:
                fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)


def _create_snapshot_commit(
    sut_dir: Path,
    run_id: str,
    iteration: int,
    *,
    snapshot_ref: str = SNAPSHOT_REF,
    message_prefix: str = "snapshot",
) -> Optional[str]:
    """
    Create a consistent snapshot commit for the SUT working directory.

    The test runner will use this commit to materialize a stable snapshot, avoiding
    testing a potentially in-progress working tree.
    """
    author_env = {
        **os.environ,
        "GIT_AUTHOR_NAME": os.environ.get("GIT_AUTHOR_NAME", "Hackathon-24h-Bench"),
        "GIT_AUTHOR_EMAIL": os.environ.get("GIT_AUTHOR_EMAIL", "hackathon-24h-bench@localhost"),
        "GIT_COMMITTER_NAME": os.environ.get("GIT_COMMITTER_NAME", "Hackathon-24h-Bench"),
        "GIT_COMMITTER_EMAIL": os.environ.get("GIT_COMMITTER_EMAIL", "hackathon-24h-bench@localhost"),
    }
    msg = f"{message_prefix}: {run_id} iter {iteration:03d}"
    temp_index_path: Optional[str] = None

    try:
        with _git_repo_lock(sut_dir):
            if not _ensure_git_repo(sut_dir):
                return None

            head_result = subprocess.run(
                ["git", "rev-parse", "--verify", "HEAD"],
                cwd=str(sut_dir),
                capture_output=True,
                text=True,
                timeout=10,
            )
            has_head = head_result.returncode == 0
            head_commit = head_result.stdout.strip() if has_head else None

            fd, temp_index_path = tempfile.mkstemp(prefix="lab_snapshot_index_")
            os.close(fd)
            # GIT_INDEX_FILE must point to a non-existent path, otherwise git
            # may treat a zero-length placeholder as a corrupted index.
            os.unlink(temp_index_path)

            snapshot_env = {
                **author_env,
                "GIT_INDEX_FILE": temp_index_path,
            }

            read_tree_cmd = ["git", "read-tree", "HEAD"] if has_head else ["git", "read-tree", "--empty"]
            read_tree = subprocess.run(
                read_tree_cmd,
                cwd=str(sut_dir),
                capture_output=True,
                text=True,
                timeout=30,
                env=snapshot_env,
            )
            if read_tree.returncode != 0:
                logger.warning(f"git read-tree 失败: {(read_tree.stderr or read_tree.stdout).strip()}")
                return None

            add_result = subprocess.run(
                [
                    "git",
                    "add",
                    "-A",
                    "--",
                    ".",
                    ":(exclude).hackathon-24h-bench.git.lock",
                    ":(exclude).lab_snapshot_index_*",
                    ":(exclude).lab_snapshot_index_*.lock",
                    ":(exclude)lab_snapshot_index_*",
                    ":(exclude)lab_snapshot_index_*.lock",
                ],
                cwd=str(sut_dir),
                capture_output=True,
                text=True,
                timeout=60,
                env=snapshot_env,
            )
            if add_result.returncode != 0:
                add_msg = (add_result.stderr or add_result.stdout).strip()
                # git add fails when :(exclude) pathspecs mention files already
                # covered by .gitignore ("Use -f if you really want to add them").
                # This is harmless — the files are already excluded — so we only
                # treat it as a real failure when the message does NOT look like
                # a simple "ignored path" hint.
                if "Use -f if you really want to add them" not in add_msg:
                    logger.warning(f"git add(快照index) 失败: {add_msg}")
                    return None
                logger.debug(f"git add(快照index) 忽略 gitignore 冲突: {add_msg}")

            tree_result = subprocess.run(
                ["git", "write-tree"],
                cwd=str(sut_dir),
                capture_output=True,
                text=True,
                timeout=30,
                env=snapshot_env,
            )
            if tree_result.returncode != 0:
                logger.warning(f"git write-tree 失败: {(tree_result.stderr or tree_result.stdout).strip()}")
                return None

            tree_id = tree_result.stdout.strip()
            if not tree_id:
                logger.warning("git write-tree 返回空 tree id")
                return None

            if has_head and head_commit:
                head_tree_result = subprocess.run(
                    ["git", "rev-parse", f"{head_commit}^{{tree}}"],
                    cwd=str(sut_dir),
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if head_tree_result.returncode == 0 and head_tree_result.stdout.strip() == tree_id:
                    # No content changes; keep current HEAD and just refresh snapshot ref.
                    update_ref = subprocess.run(
                        ["git", "update-ref", snapshot_ref, head_commit],
                        cwd=str(sut_dir),
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )
                    if update_ref.returncode != 0:
                        logger.warning(f"git update-ref 失败: {(update_ref.stderr or update_ref.stdout).strip()}")
                    return head_commit

            commit_cmd = ["git", "commit-tree", tree_id, "-m", msg]
            if has_head and head_commit:
                commit_cmd += ["-p", head_commit]
            commit_result = subprocess.run(
                commit_cmd,
                cwd=str(sut_dir),
                capture_output=True,
                text=True,
                timeout=30,
                env=author_env,
            )
            if commit_result.returncode != 0:
                logger.warning(f"git commit-tree 失败: {(commit_result.stderr or commit_result.stdout).strip()}")
                return head_commit or None

            snapshot_commit = commit_result.stdout.strip()
            if not snapshot_commit:
                logger.warning("git commit-tree 返回空 commit id")
                return head_commit or None

            update_ref = subprocess.run(
                ["git", "update-ref", snapshot_ref, snapshot_commit],
                cwd=str(sut_dir),
                capture_output=True,
                text=True,
                timeout=10,
            )
            if update_ref.returncode != 0:
                logger.warning(f"git update-ref 失败: {(update_ref.stderr or update_ref.stdout).strip()}")
            return snapshot_commit
    except Exception as e:
        logger.warning(f"创建快照提交异常: {e}")
        return _git_head_commit(sut_dir)
    finally:
        if temp_index_path:
            try:
                os.unlink(temp_index_path)
            except OSError:
                pass


def _write_latest_snapshot(
    log_manager: Optional[LogManager],
    sut_dir: Path,
    iteration: int,
    *,
    write_iteration_file: bool = True,
) -> None:
    if not log_manager:
        return
    commit = _create_snapshot_commit(sut_dir, log_manager.run_id, iteration)
    if not commit:
        return

    payload: Dict[str, Any] = {
        "run_id": log_manager.run_id,
        "iteration": iteration,
        "commit": commit,
        "snapshot_ref": SNAPSHOT_REF,
        "sut_dir": str(sut_dir),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    _atomic_write_json(log_manager.run_dir / "latest_snapshot.json", payload)
    if write_iteration_file:
        _atomic_write_json(log_manager.run_dir / "snapshots" / f"iter_{iteration:03d}.json", payload)


def _write_baseline_snapshot(log_manager: Optional[LogManager], sut_dir: Path) -> None:
    """Write a dedicated run-start baseline snapshot without touching latest_snapshot."""
    if not log_manager:
        return

    baseline_ref = _baseline_snapshot_ref(log_manager.run_id)
    commit = _create_snapshot_commit(
        sut_dir,
        log_manager.run_id,
        iteration=0,
        snapshot_ref=baseline_ref,
        message_prefix="baseline",
    )
    if not commit:
        return

    payload: Dict[str, Any] = {
        "run_id": log_manager.run_id,
        "commit": commit,
        "snapshot_ref": baseline_ref,
        "sut_dir": str(sut_dir),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "kind": "run_start_baseline",
    }
    _atomic_write_json(log_manager.run_dir / "baseline_snapshot.json", payload)


def _write_controller_done(log_manager: Optional[LogManager]) -> None:
    """Write a marker file to signal the test runner that the controller has finished."""
    if not log_manager:
        return
    payload = {
        "run_id": log_manager.run_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    marker_path = log_manager.run_dir / "controller_done.json"
    _atomic_write_json(marker_path, payload)
    logger.info("Wrote controller_done marker: %s", marker_path)


def _find_max_historical_iteration(log_manager: Optional[LogManager]) -> int:
    """
    Find the max completed historical iteration for a run.

    Data sources (best effort):
    - logs/runs/<run_id>/iterations/iter_XXX.json
    - logs/runs/<run_id>/snapshots/iter_XXX.json
    - logs/runs/<run_id>/latest_snapshot.json (field: iteration)
    """
    if not log_manager:
        return 0

    max_iter = 0

    def _collect_from_iter_dir(iter_dir: Path) -> None:
        nonlocal max_iter
        if not iter_dir.exists():
            return

        for path in iter_dir.glob("iter_*.json"):
            match = _ITER_FILE_RE.match(path.name)
            if match:
                try:
                    max_iter = max(max_iter, int(match.group(1)))
                except ValueError:
                    pass

            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                value = payload.get("iteration")
                if isinstance(value, int) and value >= 0:
                    max_iter = max(max_iter, value)
            except Exception:
                # Ignore malformed history files and continue.
                continue

    _collect_from_iter_dir(log_manager.iterations_dir)
    _collect_from_iter_dir(log_manager.run_dir / "snapshots")

    latest_snapshot = log_manager.run_dir / "latest_snapshot.json"
    if latest_snapshot.exists():
        try:
            payload = json.loads(latest_snapshot.read_text(encoding="utf-8"))
            value = payload.get("iteration")
            if isinstance(value, int) and value >= 0:
                max_iter = max(max_iter, value)
        except Exception:
            pass

    return max_iter


def load_controller_config() -> Dict[str, Any]:
    """读取全局配置中的 code_agent_controller 配置（优先 config/global.yaml）。"""
    if yaml is None:
        return {}

    candidates = [
        WORK_DIR / "config" / "global.yaml",
        WORK_DIR / "config.yaml",  # legacy path
    ]
    for config_path in candidates:
        if not config_path.exists():
            continue
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            section = raw.get("code_agent_controller") or {}
            if isinstance(section, dict):
                return section
        except Exception:
            continue
    return {}


def _parse_bool_arg(value: str) -> bool:
    """Parse boolean-like CLI argument values."""
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise argparse.ArgumentTypeError(
        "must be one of: true/false, 1/0, yes/no, on/off"
    )


def _parse_int_like(value: Any) -> Optional[int]:
    """Best-effort parse integer-like value."""
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _resolve_int_setting(
    *,
    cli_value: Optional[int],
    env_keys: tuple[str, ...],
    config: Dict[str, Any],
    config_keys: tuple[str, ...],
    default: int,
    min_value: int,
) -> int:
    """Resolve integer setting by priority: CLI > ENV > config > default."""
    if cli_value is not None:
        if cli_value < min_value:
            logger.warning(
                "CLI value %s is below minimum %s, fallback to %s",
                cli_value,
                min_value,
                default,
            )
            return default
        return cli_value

    for env_key in env_keys:
        raw = os.environ.get(env_key)
        parsed = _parse_int_like(raw)
        if parsed is None:
            if raw is not None and str(raw).strip():
                logger.warning("Invalid integer in env %s=%r, ignored", env_key, raw)
            continue
        if parsed < min_value:
            logger.warning(
                "Env %s=%s is below minimum %s, ignored",
                env_key,
                parsed,
                min_value,
            )
            continue
        return parsed

    for config_key in config_keys:
        raw = config.get(config_key)
        parsed = _parse_int_like(raw)
        if parsed is None:
            if raw is not None:
                logger.warning("Invalid integer in config %s=%r, ignored", config_key, raw)
            continue
        if parsed < min_value:
            logger.warning(
                "Config %s=%s is below minimum %s, ignored",
                config_key,
                parsed,
                min_value,
            )
            continue
        return parsed

    return default


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    available_suts = ", ".join(get_available_suts())
    parser = argparse.ArgumentParser(
        description="Code Agent Controller - 可扩展的代码代理控制器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用 Codex (默认，数据库系统)
  python -m code_agent_controller --sut-dir ./workspace/database/database_gpt

  # 使用 Claude Code
  python -m code_agent_controller --agent claude --sut-dir ./workspace/database/database_claude

  # 使用消息队列系统
  python -m code_agent_controller --system-type message_queue --sut-dir ./message_queue_gpt

  # 使用 Gemini CLI
  python -m code_agent_controller --agent gemini --sut-dir ./workspace/database/database_gemini

  # 使用 Kimi Code CLI
  python -m code_agent_controller --agent kimi --sut-dir ./workspace/database/database_kimi

  # 列出所有可用代理
  python -m code_agent_controller --list-agents

	环境变量:
	  SYSTEM_TYPE            - 默认系统类型 (database, message_queue, http_server, redis_kvstore)
  CODE_AGENT             - 默认代理类型
  CODE_AGENT_MODEL       - 默认模型名称（可选）
  OPENAI_API_KEY         - Codex 所需的 OpenAI API 密钥
  ANTHROPIC_API_KEY      - Claude Code 所需的 API 密钥（兼容）
  ANTHROPIC_AUTH_TOKEN   - Claude Gateway 鉴权令牌
  API_TIMEOUT_MS         - Claude Gateway 请求超时（毫秒，可选）
  GEMINI_API_KEY         - Gemini CLI 所需的 API 密钥
  KIMI_API_KEY           - Kimi Code CLI 所需的 API 密钥（推荐）
  CODE_AGENT_WAIT_TIME   - 改进迭代等待时间（秒）
  CODE_AGENT_MAX_RETRIES - 代理命令重试次数（最小 1）
  CODE_AGENT_COMMAND_TIMEOUT - 代理命令超时（秒，最小 1）
  CODEX_BYPASS_SANDBOX   - 设置为 true 可绕过 Codex 沙箱限制
  CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS - 设置为 true 可跳过 Claude 权限确认
"""
    )
    parser.add_argument(
        "--agent",
        default=get_env("CODE_AGENT", "codex"),
        help=f"选择代码代理类型 (默认: codex)。可选: {', '.join(get_available_agents())}"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="指定模型名称（可选，优先级最高）"
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="指定 provider 名称（可选；例如 litellm, openrouter, azure_openai 或自定义 proxy）"
    )
    parser.add_argument(
        "--system-type",
        default=get_env("SYSTEM_TYPE", "database"),
        help=f"选择系统类型 (默认: database)。可选: {available_suts}"
    )
    parser.add_argument(
        "--sut-dir",
        default="",
        help="系统工作目录（推荐；例如 ./workspace/database/database_gpt 或 ./message_queue_gpt）",
    )
    parser.add_argument(
        "--wait-time",
        type=int,
        default=None,
        help=(
            "每次改进迭代之间的等待时间（秒）。"
            "默认按优先级解析: CODE_AGENT_WAIT_TIME/AGENT_WAIT_TIME > "
            "config.wait_time > config.improvement_interval > 60"
        ),
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="最大迭代次数（0 表示无限，默认: 0）"
    )
    parser.add_argument(
        "--use-resume",
        type=_parse_bool_arg,
        default=_parse_bool_arg(get_env("AGENT_USE_RESUME", "true")),
        metavar="BOOL",
        help="改进迭代中是否使用 resume（默认: true）",
    )
    parser.add_argument(
        "--skip-init",
        action="store_true",
        help="跳过初始化检查，即使目录为空也不初始化"
    )
    parser.add_argument(
        "--init-only",
        action="store_true",
        help="仅执行初始化，不进入改进循环"
    )
    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="列出所有可用的代理并退出"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="启用详细日志输出"
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="日志文件路径"
    )
    # Docker mode arguments
    parser.add_argument(
        "--docker",
        action="store_true",
        help="在 Docker 容器中运行代理（更安全）"
    )
    parser.add_argument(
        "--docker-image",
        type=str,
        default=DEFAULT_IMAGE_NAME,
        help=f"Docker 镜像名称（默认: {DEFAULT_IMAGE_NAME}）"
    )
    parser.add_argument(
        "--build-image",
        action="store_true",
        help="在运行前构建 Docker 镜像"
    )
    parser.add_argument(
        "--detach",
        action="store_true",
        help="以后台模式运行 Docker 容器"
    )
    parser.add_argument(
        "--session-dir",
        type=str,
        default=None,
        help="Session 文件存储目录（用于 Docker 模式）"
    )
    parser.add_argument(
        "--custom-agents-dir",
        type=str,
        default=None,
        help="自定义代理目录路径"
    )
    # 日志系统参数
    parser.add_argument(
        "--log-dir",
        type=str,
        default=None,
        help="日志根目录（默认: ./logs）。指定时会覆盖 --log-file"
    )
    parser.add_argument(
        "--save-io",
        action="store_true",
        help="保存完整的输入输出到 JSON 文件"
    )
    return parser.parse_args()


def resolve_agent_model(
    cli_model: Optional[str],
    agent_name: str,
    controller_config: Dict[str, Any]
) -> Optional[str]:
    """解析最终模型名称：CLI > ENV > 全局配置。"""
    resolved: Optional[str]
    if cli_model:
        resolved = cli_model
    else:
        env_model = get_env("CODE_AGENT_MODEL")
        if env_model:
            resolved = env_model
        else:
            agent_env_map = {
                "codex": "CODEX_MODEL",
                "claude": "CLAUDE_MODEL",
                "gemini": "GEMINI_MODEL",
                "kimi": "KIMI_MODEL",
                "opencode": "OPENCODE_MODEL",
                "cline": "CLINE_MODEL",
            }
            agent_key = agent_env_map.get(agent_name.lower())
            if agent_key:
                agent_env = get_env(agent_key)
                if agent_env:
                    resolved = agent_env
                else:
                    config_model = controller_config.get("model")
                    resolved = config_model if config_model else None
            else:
                config_model = controller_config.get("model")
                resolved = config_model if config_model else None

    if agent_name.lower() == "opencode":
        from .agents.opencode import normalize_opencode_model

        return normalize_opencode_model(resolved)
    return resolved


def print_agents_list() -> None:
    """打印代理列表"""
    print("可用的代码代理:")
    print("-" * 50)
    agents_info = list_agents_info()
    for name, info in agents_info.items():
        print(f"  {name:10} - {info['doc']}")
    print("-" * 50)
    print(f"共 {len(agents_info)} 个代理")


def run_controller(
    agent_name: str,
    system_type: str,
    sut_dir: Path,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    wait_time: int = DEFAULT_WAIT_TIME_SECONDS,
    max_retries: int = DEFAULT_MAX_RETRIES,
    command_timeout: int = DEFAULT_COMMAND_TIMEOUT_SECONDS,
    init_command_timeout: int = DEFAULT_INIT_COMMAND_TIMEOUT_SECONDS,
    improve_command_timeout: int = DEFAULT_IMPROVE_COMMAND_TIMEOUT_SECONDS,
    api_timeout_ms: int = 0,
    completion_grace_seconds: int = DEFAULT_COMPLETION_GRACE_SECONDS,
    max_iterations: int = 0,
    use_resume: bool = True,
    skip_init: bool = False,
    init_only: bool = False,
    log_manager: Optional[LogManager] = None,
) -> int:
    """
    运行控制器主循环

    Args:
        agent_name: 代理名称
        sut_dir: SUT 工作目录
        model: 模型名称（可选）
        wait_time: 迭代间等待时间
        max_retries: 代理命令最大重试次数
        command_timeout: 代理命令超时时间（秒）— 通用回退值
        init_command_timeout: 初始化阶段命令超时（秒）
        improve_command_timeout: 改进迭代命令超时（秒）
        api_timeout_ms: 单次 API 请求超时（毫秒），0 表示不设置
        completion_grace_seconds: 检测到完成信号后等待进程退出的宽限期（秒）
        max_iterations: 最大迭代次数 (0 表示无限)
        use_resume: 改进迭代时是否启用 resume
        skip_init: 是否跳过初始化
        init_only: 是否仅初始化
        log_manager: 日志管理器（可选）

    Returns:
        退出码 (0 成功, 1 失败)
    """
    logger.info("=" * 60)
    logger.info("Code Agent Controller 启动")
    logger.info(f"代理类型: {agent_name}")
    logger.info(f"系统类型: {system_type}")
    logger.info(f"模型名称: {model or '默认'}")
    logger.info(f"工作目录: {sut_dir}")
    logger.info(
        "控制参数: wait_time=%ss, max_retries=%s, command_timeout=%ss"
        " (init=%ss, improve=%ss), grace=%ss",
        wait_time,
        max_retries,
        command_timeout,
        init_command_timeout,
        improve_command_timeout,
        completion_grace_seconds,
    )
    if api_timeout_ms > 0:
        logger.info("API_TIMEOUT_MS=%s", api_timeout_ms)
    logger.info(f"改进迭代使用 resume: {use_resume}")
    logger.info("=" * 60)

    # Inject API_TIMEOUT_MS into process environment (all agents inherit it)
    if api_timeout_ms > 0:
        os.environ.setdefault("API_TIMEOUT_MS", str(api_timeout_ms))

    # 验证代理名称
    available = get_available_agents()
    if agent_name.lower() not in available:
        logger.error(f"未知的代理类型: {agent_name}")
        logger.error(f"可用的代理: {', '.join(available)}")
        return 1

    # 创建代理
    try:
        agent_config = {
            "model": model,
            "system_type": system_type,
            "use_resume": use_resume,
            "max_retries": max_retries,
            "command_timeout": command_timeout,
            "init_command_timeout": init_command_timeout,
            "improve_command_timeout": improve_command_timeout,
            "completion_grace_seconds": completion_grace_seconds,
        }
        if provider:
            agent_config["provider"] = provider
        agent = create_agent(
            agent_name,
            sut_dir,
            agent_config,
        )
    except ValueError as e:
        logger.error(str(e))
        return 1

    # 设置日志管理器
    if log_manager:
        agent.log_manager = log_manager

    # 检查 CLI 工具
    if not agent.check_cli():
        return 1

    # 检查 API 密钥（并执行必要的登录）
    if not agent.check_api_key():
        return 1

    # 确保 SUT 工作目录存在
    ensure_directory(sut_dir)

    # 检查是否已经初始化
    has_init = has_sut_files(sut_dir)
    if has_init:
        logger.info("检测到已有 SUT 实现文件，跳过初始化")

    # Determine iteration start before writing new snapshots for this process.
    max_historical_iteration = _find_max_historical_iteration(log_manager)
    start_iteration = max_historical_iteration + 1 if max_historical_iteration > 0 else 1
    if max_historical_iteration > 0:
        logger.info(
            f"检测到历史最大迭代: {max_historical_iteration}，将从迭代 {start_iteration} 继续"
        )

    # 初始化 SUT（如果还没有）
    if not has_init and not skip_init:
        _write_baseline_snapshot(log_manager, sut_dir)
        if not agent.initialize():
            logger.error("初始化失败，退出")
            return 1
        _write_latest_snapshot(log_manager, sut_dir, iteration=0)
        time.sleep(2)
    else:
        # 目录已存在或跳过初始化：创建一次稳定快照，但不要把 latest 回退到 iter_000。
        # 如果已有历史迭代，latest 的 iteration 对齐到历史最大值，且不覆盖历史迭代文件。
        bootstrap_iteration = max_historical_iteration if max_historical_iteration > 0 else 0
        _write_latest_snapshot(
            log_manager,
            sut_dir,
            iteration=bootstrap_iteration,
            write_iteration_file=(bootstrap_iteration == 0),
        )

    # 仅初始化模式
    if init_only:
        logger.info("初始化完成，退出（--init-only 模式）")
        return 0

    # 改进循环
    iteration = start_iteration
    completed_iterations = 0
    while True:
        try:
            logger.info(f"\n{'=' * 60}")
            logger.info(f"开始改进循环 - 迭代 {iteration}")
            logger.info(f"{'=' * 60}\n")

            success = agent.improve(iteration)
            effective_wait_time = wait_time
            if success:
                _write_latest_snapshot(log_manager, sut_dir, iteration=iteration)
                iteration += 1
                completed_iterations += 1
            else:
                if _is_rate_limit_error_from_result(getattr(agent, "last_command_result", None)):
                    effective_wait_time = RATE_LIMIT_WAIT_TIME_SECONDS
                    logger.warning(
                        f"检测到 429 / rate limit，本次等待时间调整为 {effective_wait_time} 秒"
                    )
                logger.info(f"迭代 {iteration} 执行失败，不增加迭代计数，将在等待后重试同一迭代")

            # 检查是否达到本次运行的最大迭代次数
            if max_iterations > 0 and completed_iterations >= max_iterations:
                logger.info(f"已达到最大迭代次数 ({max_iterations})，退出")
                break

            logger.info(f"等待 {effective_wait_time} 秒后进行下一次改进...")
            time.sleep(effective_wait_time)

        except KeyboardInterrupt:
            logger.info("\n收到中断信号，退出...")
            break
        except Exception as e:
            logger.error(f"发生错误: {e}", exc_info=True)
            logger.info("等待30秒后继续...")
            time.sleep(30)

    _write_controller_done(log_manager)
    return 0


def run_docker_controller(
    agent_name: str,
    system_type: str,
    sut_dir: Path,
    model: Optional[str] = None,
    wait_time: int = DEFAULT_WAIT_TIME_SECONDS,
    max_iterations: int = 0,
    use_resume: bool = True,
    skip_init: bool = False,
    init_only: bool = False,
    docker_image: str = DEFAULT_IMAGE_NAME,
    build_image: bool = False,
    detach: bool = False,
    session_dir: Optional[Path] = None,
    custom_agents_dir: Optional[Path] = None,
) -> int:
    """
    Run controller in Docker mode.

    Args:
        agent_name: Agent name
        sut_dir: SUT working directory
        model: Model name
        wait_time: Wait time between iterations
        max_iterations: Maximum iterations
        use_resume: Whether to use resume in improve iterations
        skip_init: Skip initialization
        init_only: Only initialize
        docker_image: Docker image name
        build_image: Whether to build image first
        detach: Run in background
        session_dir: Session files directory
        custom_agents_dir: Custom agents directory

    Returns:
        Exit code
    """
    logger.info("=" * 60)
    logger.info("Code Agent Controller (Docker Mode) 启动")
    logger.info(f"代理类型: {agent_name}")
    logger.info(f"模型名称: {model or '默认'}")
    logger.info(f"工作目录: {sut_dir}")
    logger.info(f"Docker 镜像: {docker_image}")
    logger.info("=" * 60)

    # Check Docker availability
    if not check_docker_available():
        logger.error("Docker 不可用，请先安装 Docker")
        return 1

    # Create Docker runner
    runner = DockerAgentRunner(
        sut_dir=sut_dir,
        session_dir=session_dir,
        custom_agents_dir=custom_agents_dir,
        image_name=docker_image,
        system_type=system_type,
    )

    # Build image if requested or if it doesn't exist
    if build_image or not runner.image_exists():
        logger.info("正在构建 Docker 镜像...")
        if not runner.build_image(build_args={"TARGET_AGENT": agent_name.lower()}):
            logger.error("Docker 镜像构建失败")
            return 1

    # Run agent in container
    success = runner.run_agent(
        agent_type=agent_name,
        model=model,
        wait_time=wait_time,
        max_iterations=max_iterations,
        skip_init=skip_init,
        init_only=init_only,
        detach=detach,
        extra_args=[
            "--system-type", system_type,
            "--use-resume", "true" if use_resume else "false",
        ],
    )

    return 0 if success else 1


def main() -> int:
    """
    主入口函数

    Returns:
        退出码
    """
    # 加载环境变量
    load_env_file()

    # 读取配置文件
    controller_config = load_controller_config()

    # 解析参数
    args = parse_args()
    os.environ["SYSTEM_TYPE"] = (args.system_type or "database").strip()
    system_type_str = (args.system_type or "database").strip()

    # 列出代理（提前处理，避免日志初始化）
    if args.list_agents:
        # Load custom agents first
        custom_dir = Path(args.custom_agents_dir) if args.custom_agents_dir else None
        load_custom_agents(custom_dir)
        print_agents_list()
        return 0

    # 解析模型名称（在日志初始化前完成，以便 run_id / 日志目录名包含模型信息）
    model = resolve_agent_model(args.model, args.agent, controller_config)
    provider_hint = getattr(args, "provider", None)
    resolved_wait_time = _resolve_int_setting(
        cli_value=args.wait_time,
        env_keys=("CODE_AGENT_WAIT_TIME", "AGENT_WAIT_TIME"),
        config=controller_config,
        config_keys=("wait_time", "improvement_interval"),
        default=DEFAULT_WAIT_TIME_SECONDS,
        min_value=0,
    )
    resolved_max_retries = _resolve_int_setting(
        cli_value=None,
        env_keys=("CODE_AGENT_MAX_RETRIES", "AGENT_MAX_RETRIES"),
        config=controller_config,
        config_keys=("max_retries",),
        default=DEFAULT_MAX_RETRIES,
        min_value=1,
    )
    resolved_command_timeout = _resolve_int_setting(
        cli_value=None,
        env_keys=("CODE_AGENT_COMMAND_TIMEOUT", "AGENT_COMMAND_TIMEOUT"),
        config=controller_config,
        config_keys=("command_timeout",),
        default=DEFAULT_COMMAND_TIMEOUT_SECONDS,
        min_value=1,
    )
    resolved_init_timeout = _resolve_int_setting(
        cli_value=None,
        env_keys=("CODE_AGENT_INIT_TIMEOUT", "AGENT_INIT_TIMEOUT"),
        config=controller_config,
        config_keys=("init_command_timeout",),
        default=resolved_command_timeout,
        min_value=1,
    )
    resolved_improve_timeout = _resolve_int_setting(
        cli_value=None,
        env_keys=("CODE_AGENT_IMPROVE_TIMEOUT", "AGENT_IMPROVE_TIMEOUT"),
        config=controller_config,
        config_keys=("improve_command_timeout",),
        default=resolved_command_timeout,
        min_value=1,
    )
    resolved_api_timeout_ms = _resolve_int_setting(
        cli_value=None,
        env_keys=("API_TIMEOUT_MS",),
        config=controller_config,
        config_keys=("api_timeout_ms",),
        default=0,
        min_value=0,
    )
    resolved_grace_seconds = _resolve_int_setting(
        cli_value=None,
        env_keys=("COMPLETION_GRACE_SECONDS",),
        config=controller_config,
        config_keys=("completion_grace_seconds",),
        default=DEFAULT_COMPLETION_GRACE_SECONDS,
        min_value=1,
    )

    # 解析系统工作目录（默认会根据 system-type 调整；也允许全局配置覆盖默认目录）
    explicit_sut_dir = bool((args.sut_dir or "").strip())
    sut_dir_arg = (args.sut_dir or "").strip()
    if not sut_dir_arg:
        config_sut_dir = controller_config.get("sut_dir")
        config_legacy_database_dir = controller_config.get("database_dir")
        picked = None
        if isinstance(config_sut_dir, str) and config_sut_dir.strip():
            picked = config_sut_dir.strip()
        elif isinstance(config_legacy_database_dir, str) and config_legacy_database_dir.strip():
            picked = config_legacy_database_dir.strip()
        if picked:
            sut_dir_arg = picked
        elif system_type_str and system_type_str != "database":
            try:
                from sut import load_config as load_sut_config

                target_dir = load_sut_config(system_type_str).get_target_dir()
                sut_dir_arg = str(target_dir)
            except Exception:
                pass

    sut_dir = Path(sut_dir_arg).expanduser()
    if not sut_dir.is_absolute():
        sut_dir = (WORK_DIR / sut_dir).resolve()

    # If using base workspace dir and no explicit per-run directory was provided,
    # materialize ./workspace/{system_type}/{run_id}.
    run_id = None
    if not explicit_sut_dir and _is_workspace_base_dir(sut_dir, system_type_str):
        run_id = _resolve_or_make_run_id(system_type_str, args.agent, model)
        os.environ["AGENT_RUN_ID"] = run_id
        sut_dir = (sut_dir / run_id).resolve()

    # Load custom agents
    custom_agents_dir = Path(args.custom_agents_dir) if args.custom_agents_dir else None
    load_custom_agents(custom_agents_dir)

    # 配置日志
    log_level = logging.DEBUG if args.verbose else logging.INFO

    # 如果指定了 --log-dir，使用 LogManager 管理日志
    log_manager = None
    if args.log_dir:
        if not run_id:
            run_id = _resolve_or_make_run_id(system_type_str, args.agent, model)
            os.environ["AGENT_RUN_ID"] = run_id

        log_manager = LogManager(
            base_dir=Path(args.log_dir),
            agent=args.agent,
            model=model,
            save_io=args.save_io,
            run_id=run_id,  # 传递 run_id
            system_type=system_type_str,  # 传递 system_type
        )
        log_file = log_manager.setup()
        setup_logging(level=log_level, log_file=str(log_file))
        logger.info(f"运行ID: {run_id}")
        logger.info(f"日志目录: {log_manager.run_dir}")
        if args.save_io:
            logger.info("已启用迭代输入输出保存")
    else:
        setup_logging(level=log_level, log_file=args.log_file)

    logger.info(
        "已解析控制参数: wait_time=%ss, max_retries=%s, command_timeout=%ss"
        " (init=%ss, improve=%ss), grace=%ss, api_timeout_ms=%s",
        resolved_wait_time,
        resolved_max_retries,
        resolved_command_timeout,
        resolved_init_timeout,
        resolved_improve_timeout,
        resolved_grace_seconds,
        resolved_api_timeout_ms,
    )

    # Docker mode
    if args.docker:
        os.environ["CODE_AGENT_WAIT_TIME"] = str(resolved_wait_time)
        os.environ["CODE_AGENT_MAX_RETRIES"] = str(resolved_max_retries)
        os.environ["CODE_AGENT_COMMAND_TIMEOUT"] = str(resolved_command_timeout)
        os.environ["CODE_AGENT_INIT_TIMEOUT"] = str(resolved_init_timeout)
        os.environ["CODE_AGENT_IMPROVE_TIMEOUT"] = str(resolved_improve_timeout)
        os.environ["COMPLETION_GRACE_SECONDS"] = str(resolved_grace_seconds)
        if resolved_api_timeout_ms > 0:
            os.environ.setdefault("API_TIMEOUT_MS", str(resolved_api_timeout_ms))
        session_dir = Path(args.session_dir) if args.session_dir else None
        return run_docker_controller(
            agent_name=args.agent,
            system_type=args.system_type,
            sut_dir=sut_dir,
            model=model,
            wait_time=resolved_wait_time,
            max_iterations=args.max_iterations,
            use_resume=args.use_resume,
            skip_init=args.skip_init,
            init_only=args.init_only,
            docker_image=args.docker_image,
            build_image=args.build_image,
            detach=args.detach,
            session_dir=session_dir,
            custom_agents_dir=custom_agents_dir,
        )

    # Normal mode - run controller directly
    return run_controller(
        agent_name=args.agent,
        system_type=args.system_type,
        sut_dir=sut_dir,
        model=model,
        provider=provider_hint,
        wait_time=resolved_wait_time,
        max_retries=resolved_max_retries,
        command_timeout=resolved_command_timeout,
        init_command_timeout=resolved_init_timeout,
        improve_command_timeout=resolved_improve_timeout,
        api_timeout_ms=resolved_api_timeout_ms,
        completion_grace_seconds=resolved_grace_seconds,
        max_iterations=args.max_iterations,
        use_resume=args.use_resume,
        skip_init=args.skip_init,
        init_only=args.init_only,
        log_manager=log_manager,
    )


if __name__ == "__main__":
    sys.exit(main())
