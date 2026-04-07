"""
工具函数模块

提供环境变量加载、日志配置等通用功能。
"""

import os
import sys
import json
import logging
import subprocess
import threading
import queue
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Sequence, Callable


# 工作目录
WORK_DIR = Path(__file__).parent.parent.resolve()
ENV_FILE = WORK_DIR / ".env"


def setup_logging(
    level: int = logging.INFO,
    log_file: str = None
) -> logging.Logger:
    """
    配置日志系统

    Args:
        level: 日志级别
        log_file: 可选的日志文件路径

    Returns:
        配置好的 logger 实例
    """
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    return logging.getLogger(__name__)


def load_env_file(path: Path = None) -> None:
    """
    从 .env 文件加载 KEY=VALUE 对到 os.environ

    只有当环境变量尚未设置时才会加载。

    Args:
        path: .env 文件路径，默认为项目根目录下的 .env
    """
    if path is None:
        path = ENV_FILE
    if not path.exists():
        return

    logger = logging.getLogger(__name__)
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception as exc:
        logger.warning(f"加载 .env 失败: {exc}")


def get_env(key: str, default: str = None) -> str:
    """
    获取环境变量值

    Args:
        key: 环境变量名
        default: 默认值

    Returns:
        环境变量值或默认值
    """
    return os.environ.get(key, default)


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    获取布尔类型的环境变量

    Args:
        key: 环境变量名
        default: 默认值

    Returns:
        布尔值
    """
    val = os.environ.get(key, "").lower()
    if val in ("true", "1", "yes", "on"):
        return True
    elif val in ("false", "0", "no", "off"):
        return False
    return default


def get_config_string(
    config: Optional[Dict[str, Any]],
    key: str,
    *env_keys: str,
    default: Optional[str] = None
) -> Optional[str]:
    """
    Get a string configuration value with fallback chain.

    Tries to get value from:
    1. config dict (if provided)
    2. Environment variables (in order provided)
    3. Default value

    Args:
        config: Configuration dictionary (may be None)
        key: Key to look up in config dict
        *env_keys: Environment variable names to try (in order)
        default: Default value if nothing found

    Returns:
        Configuration value or default

    Example:
        >>> model = get_config_string(config, "model", "CODEX_MODEL", "CODE_AGENT_MODEL")
    """
    # Try config dict first
    if config:
        value = config.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    # Try environment variables
    for env_key in env_keys:
        value = os.environ.get(env_key)
        if value and value.strip():
            return value.strip()

    return default


def get_config_int(
    config: Optional[Dict[str, Any]],
    key: str,
    *env_keys: str,
    default: int = 0
) -> int:
    """
    Get an integer configuration value with fallback chain.

    Args:
        config: Configuration dictionary (may be None)
        key: Key to look up in config dict
        *env_keys: Environment variable names to try (in order)
        default: Default value if nothing found

    Returns:
        Configuration value or default
    """
    # Try config dict first
    if config:
        value = config.get(key)
        if value is not None:
            try:
                return int(value)
            except (ValueError, TypeError):
                pass

    # Try environment variables
    for env_key in env_keys:
        value = os.environ.get(env_key)
        if value:
            try:
                return int(value.strip())
            except (ValueError, TypeError):
                pass

    return default


def ensure_directory(path: Path) -> None:
    """
    确保目录存在，如果不存在则创建

    Args:
        path: 目录路径
    """
    path.mkdir(parents=True, exist_ok=True)


def has_sut_files(sut_dir: Path) -> bool:
    """
    检查 SUT 工作目录中是否存在代码文件

    Args:
        sut_dir: SUT 工作目录

    Returns:
        是否存在 Python 或 shell 脚本文件
    """
    if not sut_dir.exists():
        return False
    files = list(sut_dir.glob("*.py")) + list(sut_dir.glob("*.sh"))
    return len(files) > 0




@dataclass
class CommandResult:
    """
    命令执行结果

    Attributes:
        success: 是否成功
        stdout: 标准输出
        stderr: 错误输出
        return_code: 返回码
        duration_seconds: 执行时长（秒）
    """
    success: bool
    stdout: str = ""
    stderr: str = ""
    return_code: int = 0
    duration_seconds: float = 0.0


@dataclass
class StreamingProcessResult:
    """
    流式子进程执行结果

    Attributes:
        return_code: 子进程返回码
        stdout: 完整标准输出
        stderr: 完整错误输出
        duration_seconds: 执行时长（秒）
        timed_out: 是否超时
        result_detected: 是否检测到完成信号（如 ``{"type":"result"}``）
        grace_killed: 检测到完成信号后进程未退出，被 grace-kill 终止
    """
    return_code: int
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool = False
    result_detected: bool = False
    grace_killed: bool = False


def run_subprocess_streaming(
    cmd: Sequence[str],
    *,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    input_text: Optional[str] = None,
    timeout: Optional[float] = None,
    logger: Optional[logging.Logger] = None,
    log_prefix: str = "agent-cli",
    completion_pattern: Optional[Callable[[str], bool]] = None,
    completion_grace_seconds: float = 30.0,
) -> StreamingProcessResult:
    """
    以流式方式执行子进程，实时转发 stdout/stderr 到日志。

    Args:
        completion_pattern: 可选的回调函数，接收 stdout 行（去除尾部换行）并返回
            ``True`` 表示检测到逻辑完成信号。检测到后启动 grace period，
            若进程在 *completion_grace_seconds* 内未退出则被 kill。
        completion_grace_seconds: 检测到完成信号后等待进程退出的宽限期（秒）。
    """
    start = time.time()
    stdout_chunks: List[str] = []
    stderr_chunks: List[str] = []
    events: "queue.Queue[tuple[str, Optional[str]]]" = queue.Queue()

    proc = subprocess.Popen(
        list(cmd),
        cwd=cwd,
        env=env,
        stdin=subprocess.PIPE if input_text is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    if input_text is not None and proc.stdin is not None:
        try:
            proc.stdin.write(input_text)
            proc.stdin.flush()
        finally:
            proc.stdin.close()

    def _reader(stream, source: str) -> None:
        try:
            for line in iter(stream.readline, ""):
                events.put((source, line))
        finally:
            try:
                stream.close()
            except Exception:
                pass
            events.put((source, None))

    stdout_thread = threading.Thread(target=_reader, args=(proc.stdout, "stdout"), daemon=True)
    stderr_thread = threading.Thread(target=_reader, args=(proc.stderr, "stderr"), daemon=True)
    stdout_thread.start()
    stderr_thread.start()

    finished_streams = 0
    timed_out = False
    result_detected_at: Optional[float] = None
    grace_killed = False

    while finished_streams < 2:
        remaining = None
        if timeout is not None:
            deadline = start + timeout
            remaining = deadline - time.time()
            if remaining <= 0:
                timed_out = True
                proc.kill()
                break

        # Grace period: result detected but process still alive
        if result_detected_at is not None:
            grace_remaining = (result_detected_at + completion_grace_seconds) - time.time()
            if grace_remaining <= 0:
                if logger:
                    logger.warning(
                        "[%s] Process did not exit within %ss after completion signal, killing",
                        log_prefix,
                        completion_grace_seconds,
                    )
                grace_killed = True
                proc.kill()
                break
            # Tighten poll interval during grace period
            if remaining is None:
                remaining = grace_remaining
            else:
                remaining = min(remaining, grace_remaining)

        try:
            wait_for = 0.2 if remaining is None else max(0.01, min(0.2, remaining))
            source, payload = events.get(timeout=wait_for)
        except queue.Empty:
            continue

        if payload is None:
            finished_streams += 1
            continue

        line = payload.rstrip("\n")
        if source == "stdout":
            stdout_chunks.append(payload)
            if logger and line:
                logger.info("[%s][stdout] %s", log_prefix, line)
            # Detect completion signal
            if completion_pattern and result_detected_at is None:
                try:
                    if completion_pattern(line):
                        result_detected_at = time.time()
                        if logger:
                            logger.info(
                                "[%s] Completion signal detected, grace period %ss",
                                log_prefix,
                                completion_grace_seconds,
                            )
                except Exception:
                    pass
        else:
            stderr_chunks.append(payload)
            if logger and line:
                logger.error("[%s][stderr] %s", log_prefix, line)

    if timed_out or grace_killed:
        try:
            proc.wait(timeout=5)
        except Exception:
            pass
    elif proc.returncode is None:
        # Streams may have ended before returncode is populated; wait briefly to
        # collect the real process exit status instead of falling back to -1.
        try:
            proc.wait(timeout=5)
        except Exception:
            pass

    stdout_thread.join(timeout=1)
    stderr_thread.join(timeout=1)

    return_code = proc.returncode if proc.returncode is not None else -1
    result_detected = result_detected_at is not None

    # Grace kill: agent's work was done (result output), normalize to success
    if grace_killed:
        return_code = 0
        timed_out = False

    return StreamingProcessResult(
        return_code=return_code,
        stdout="".join(stdout_chunks),
        stderr="".join(stderr_chunks),
        duration_seconds=time.time() - start,
        timed_out=timed_out,
        result_detected=result_detected,
        grace_killed=grace_killed,
    )


class LogManager:
    """
    日志管理器

    管理运行日志目录结构，支持保存迭代输入输出到 JSON 文件。

    目录结构:
        logs/
        ├── runs/
        │   └── {system_type}_{agent}_{model}_{YYYYMMDD_HHMMSS}/
        │       ├── controller.log          # 控制器主日志
        │       ├── test_runner.log         # 测试运行日志（可选）
        │       └── iterations/             # 迭代详情（启用 --save-io 时）
        │           ├── iter_001.json       # 第1次迭代
        │           └── ...
        └── latest -> runs/{最新运行目录}   # 符号链接
    """

    def __init__(
        self,
        base_dir: Path,
        agent: str,
        model: Optional[str] = None,
        save_io: bool = False,
        run_id: Optional[str] = None,
        system_type: Optional[str] = None,
    ):
        """
        初始化日志管理器

        Args:
            base_dir: 日志根目录
            agent: 代理名称
            model: 模型名称（可选）
            save_io: 是否保存完整输入输出
            run_id: 运行ID（可选，如果提供则使用，否则自动生成）
            system_type: 系统类型（可选，默认从环境变量获取）
        """
        self.base_dir = Path(base_dir)
        self.agent = agent
        self.save_io = save_io
        self.system_type = system_type or os.environ.get("SYSTEM_TYPE", "database")

        # Get model from parameter or environment variables (never use "default")
        if model:
            self.model = self._sanitize_model_name(model)
        else:
            # Try agent-specific env vars first, then generic
            agent_upper = agent.upper()
            env_model = (
                os.environ.get(f"{agent_upper}_MODEL") or
                os.environ.get("CODE_AGENT_MODEL") or
                "unknown"  # Fallback if no model specified
            )
            self.model = self._sanitize_model_name(env_model)

        # 如果提供了 run_id，使用它；否则自动生成（包含 system_type）
        if run_id:
            self.run_id = run_id
        else:
            self.run_id = f"{self.system_type}_{agent}_{self.model}_{datetime.now():%Y%m%d_%H%M%S}"

        self.run_dir = self.base_dir / "runs" / self.run_id
        self.iterations_dir = self.run_dir / "iterations"
        self._iteration_count = 0

    def _sanitize_model_name(self, model: str) -> str:
        """清理模型名称，移除不适合作为文件名的字符"""
        # 替换路径分隔符和特殊字符
        sanitized = model.replace("/", "-").replace("\\", "-")
        sanitized = sanitized.replace(":", "-").replace(" ", "_")
        return sanitized

    def setup(self) -> Path:
        """
        创建目录结构并配置日志

        Returns:
            controller.log 文件路径
        """
        self.run_dir.mkdir(parents=True, exist_ok=True)
        if self.save_io:
            self.iterations_dir.mkdir(exist_ok=True)

        # 更新 latest 符号链接
        latest = self.base_dir / "latest"
        try:
            if latest.is_symlink() or latest.exists():
                latest.unlink()
            # 使用相对路径创建符号链接
            latest.symlink_to(Path("runs") / self.run_id)
        except OSError as e:
            # 符号链接创建失败不是致命错误
            logger = logging.getLogger(__name__)
            logger.warning(f"无法创建 latest 符号链接: {e}")

        return self.run_dir / "controller.log"

    def get_log_file_path(self) -> Path:
        """获取 controller.log 文件路径"""
        return self.run_dir / "controller.log"

    def get_test_runner_log_path(self) -> Path:
        """获取 test_runner.log 文件路径"""
        return self.run_dir / "test_runner.log"

    def save_iteration(
        self,
        iteration: int,
        prompt: str,
        use_resume: bool,
        session_id: Optional[str],
        result: CommandResult
    ) -> None:
        """
        保存迭代IO到JSON文件

        Args:
            iteration: 迭代次数
            prompt: 提示内容
            use_resume: 是否使用 resume 模式
            session_id: session ID
            result: 命令执行结果
        """
        if not self.save_io:
            return

        self._iteration_count = iteration
        data: Dict[str, Any] = {
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent,
            "model": self.model,
            "input": {
                "prompt": prompt,
                "use_resume": use_resume,
                "session_id": session_id or ""
            },
            "output": {
                "success": result.success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.return_code,
                "duration_seconds": result.duration_seconds
            }
        }

        try:
            path = self.iterations_dir / f"iter_{iteration:03d}.json"
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"保存迭代IO失败: {e}")

    @property
    def iteration_count(self) -> int:
        """获取当前迭代次数"""
        return self._iteration_count
