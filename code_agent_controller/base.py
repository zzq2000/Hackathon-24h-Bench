"""
代码代理基类模块

定义所有代码代理实现必须遵循的抽象接口。
"""

import os
import re
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any, Union, Tuple

from .utils import WORK_DIR, get_env, get_env_bool, get_config_int, get_config_string, CommandResult, LogManager

logger = logging.getLogger(__name__)


def is_container_mode() -> bool:
    """
    Check if running in container mode.

    Returns:
        True if CONTAINER_MODE environment variable is set to true
    """
    return get_env_bool("CONTAINER_MODE", False)


def get_session_dir() -> Path:
    """
    Get the session directory path.

    In container mode, uses SESSION_DIR environment variable.
    Otherwise uses the default WORK_DIR.

    Returns:
        Path to session directory
    """
    if is_container_mode():
        session_dir = os.environ.get("SESSION_DIR")
        if session_dir:
            return Path(session_dir)
    return WORK_DIR


def get_container_workdir(system_type: Optional[str] = None) -> str:
    """
    Get the container working directory for SUT files.

    Args:
        system_type: Optional system type (database, message_queue, etc.)
                    If not provided, uses SYSTEM_TYPE env var or defaults to database.

    Returns:
        Container SUT directory path
    """
    if system_type is None:
        system_type = os.environ.get("SYSTEM_TYPE", "database")
    return f"/workspace/{system_type}"


class CodeAgentBase(ABC):
    """
    代码代理抽象基类

    所有代码代理实现都需要继承此类并实现抽象方法。
    这是扩展新代理类型的接口定义。

    Attributes:
        name: 代理名称，用于标识和日志
        sut_dir: SUT（System Under Test）工作目录
        config: 配置字典
        session_id_file: session ID 保存文件路径
        brief_summary_dir: 测试结果简要目录路径
        brief_summary_file: 测试结果简要文件路径（默认指向 `last_brief_1.txt`）
        log_manager: 日志管理器（可选）

    Example:
        >>> class MyCustomAgent(CodeAgentBase):
        ...     name = "custom"
        ...
        ...     def check_cli(self) -> bool:
        ...         # 检查 CLI 工具
        ...         pass
        ...
        ...     def check_api_key(self) -> bool:
        ...         # 检查 API 密钥
        ...         pass
        ...
        ...     def run_command(self, prompt, use_resume=False, max_retries=3) -> CommandResult:
        ...         # 执行命令
        ...         pass
    """

    # 代理名称，子类必须覆盖
    name: str = "base"

    # Default max chars for log truncation; subclasses can override (e.g. Codex uses -1)
    _DEFAULT_LOG_MAX_CHARS: int = 8000

    @classmethod
    def _truncate_for_log(cls, text: str) -> str:
        """Truncate long output in controller.log to keep logs readable.

        Controlled by CODE_AGENT_LOG_OUTPUT_MAX_CHARS env var.
        Subclasses can override _DEFAULT_LOG_MAX_CHARS (<=0 means no truncation).
        """
        try:
            max_chars = int(os.environ.get("CODE_AGENT_LOG_OUTPUT_MAX_CHARS", str(cls._DEFAULT_LOG_MAX_CHARS)))
        except (TypeError, ValueError):
            max_chars = cls._DEFAULT_LOG_MAX_CHARS

        if max_chars <= 0 or len(text) <= max_chars:
            return text

        head = max_chars // 2
        tail = max_chars - head
        omitted = len(text) - max_chars
        return f"{text[:head]}\n...[truncated {omitted} chars]...\n{text[-tail:]}"

    @staticmethod
    def _is_no_previous_session_error(stdout: str, stderr: str) -> bool:
        """Check whether agent reports no resumable session in current project context."""
        text = f"{stdout}\n{stderr}".lower()
        return (
            "no previous sessions found for this project" in text
            or "no previous sessions found" in text
            or "no sessions found for this project" in text
            or "no sessions found" in text
            or "could not find a previous session" in text
            or "session not found" in text
            or "invalid session" in text
        )

    @staticmethod
    def _extract_session_id_json(
        output: str,
        keys: tuple = ("session_id", "sessionId", "session", "id"),
        min_length: int = 8,
    ) -> Optional[str]:
        """Extract session ID from JSON lines in output."""
        try:
            for line in output.split("\n"):
                line = line.strip()
                if not line or not line.startswith("{"):
                    continue
                if not ("session" in line.lower() or "id" in line.lower()):
                    continue
                try:
                    import json as _json
                    data = _json.loads(line)
                    for key in keys:
                        value = data.get(key)
                        if isinstance(value, str) and len(value.strip()) >= min_length:
                            return value.strip()
                except (ValueError, KeyError):
                    continue
        except Exception:
            pass
        return None

    @staticmethod
    def _extract_session_id_regex(output: str, patterns: tuple) -> Optional[str]:
        """Extract session ID using regex patterns."""
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _resolve_model(self, config: Optional[Dict[str, Any]], *env_keys: str) -> Optional[str]:
        """Resolve model name from config dict and env vars.

        Usage: self.model = self._resolve_model(config, "CLAUDE_MODEL", "CODE_AGENT_MODEL")
        """
        return get_config_string(config, "model", *env_keys)

    @staticmethod
    def _parse_use_resume(value: Any, default: bool = True) -> bool:
        """Parse use_resume from bool-like config values."""
        if isinstance(value, bool):
            return value
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on"}:
                return True
            if normalized in {"0", "false", "no", "off"}:
                return False
        return default

    @staticmethod
    def _sanitize_session_scope(value: str) -> str:
        """
        Sanitize run/session scope value for filesystem path.

        Keeps common safe characters and replaces others with "_".
        """
        return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._-") or "default"

    @staticmethod
    def _resolve_session_scope() -> str:
        """
        Resolve session scope for persistent resume context.

        Priority:
        1. AGENT_SESSION_SCOPE (stable scope across restarts)
        2. AGENT_RUN_ID
        3. default
        """
        scope = (os.environ.get("AGENT_SESSION_SCOPE") or "").strip()
        if scope:
            return scope
        run_id = (os.environ.get("AGENT_RUN_ID") or "").strip()
        if run_id:
            return run_id
        return "default"

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        """
        初始化代码代理

        Args:
            sut_dir: SUT（System Under Test）工作目录
            config: 可选的配置字典
        """
        self.sut_dir = sut_dir
        self.config = config or {}
        self.iteration_use_resume = self._parse_use_resume(self.config.get("use_resume"), default=True)
        self.max_retries = get_config_int(
            self.config,
            "max_retries",
            "CODE_AGENT_MAX_RETRIES",
            "AGENT_MAX_RETRIES",
            default=3,
        )
        if self.max_retries < 1:
            logger.warning("max_retries=%s 非法，回退为 3", self.max_retries)
            self.max_retries = 3
        self.command_timeout = get_config_int(
            self.config,
            "command_timeout",
            "CODE_AGENT_COMMAND_TIMEOUT",
            "AGENT_COMMAND_TIMEOUT",
            default=300,
        )
        if self.command_timeout < 1:
            logger.warning("command_timeout=%s 非法，回退为 300", self.command_timeout)
            self.command_timeout = 300
        # Use session directory (container-aware)
        session_dir = get_session_dir()
        self.session_scope = self._resolve_session_scope()
        scoped_dir = session_dir / self._sanitize_session_scope(self.session_scope)
        self.session_id_file = scoped_dir / f".{self.name}_session_id"
        self.session_meta_file = scoped_dir / f".{self.name}_session_meta.json"
        self.brief_summary_dir = sut_dir / "last_brief"
        self.brief_summary_file = self.brief_summary_dir / "last_brief_1.txt"
        self._container_mode = is_container_mode()
        # 日志管理器（由控制器设置）
        self.log_manager: Optional[LogManager] = None
        # 最近一次命令执行结果（供控制器判断重试节奏）
        self.last_command_result: Optional[CommandResult] = None

    @abstractmethod
    def check_cli(self) -> bool:
        """
        检查 CLI 工具是否已安装

        Returns:
            是否已安装
        """
        pass

    @abstractmethod
    def check_api_key(self) -> bool:
        """
        检查 API 密钥是否已设置

        Returns:
            是否已设置
        """
        pass

    @abstractmethod
    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """
        运行代理命令

        Args:
            prompt: 给代理的提示
            use_resume: 是否使用 resume 模式继续之前的会话
            max_retries: 最大重试次数

        Returns:
            CommandResult 对象，包含执行结果详情
        """
        pass

    @staticmethod
    def _extract_brief_index(file_path: Path) -> Optional[int]:
        """Extract numeric index from last_brief_<i>.txt filename."""
        match = re.match(r"^last_brief_(\d+)\.txt$", file_path.name)
        if not match:
            return None
        index = int(match.group(1))
        return index if index > 0 else None

    def _get_latest_brief_summary_file(self) -> Optional[Path]:
        """Get latest brief file from ./last_brief/, with legacy fallback."""
        latest_file: Optional[Path] = None
        max_index = 0
        if self.brief_summary_dir.is_dir():
            for file_path in self.brief_summary_dir.iterdir():
                if not file_path.is_file():
                    continue
                index = self._extract_brief_index(file_path)
                if index and index > max_index:
                    max_index = index
                    latest_file = file_path

        if latest_file is not None:
            return latest_file

        legacy_file = self.sut_dir / "last_brief.txt"
        if legacy_file.exists():
            return legacy_file
        return None

    def _read_latest_brief_summary(self) -> Tuple[str, Optional[Path]]:
        """Read latest brief summary content and return content with file path."""
        brief_file = self._get_latest_brief_summary_file()
        if brief_file is None:
            return "", None
        try:
            return brief_file.read_text(encoding="utf-8").strip(), brief_file
        except Exception as e:
            logger.warning(f"读取简要测试结果失败: {e}")
            return "", brief_file

    def get_workdir(self) -> str:
        """
        获取代理实际工作目录，用于提示文案

        Returns:
            工作目录路径字符串
        """
        if self._container_mode:
            return get_container_workdir()
        return str(self.sut_dir)

    def is_in_container(self) -> bool:
        """
        检查是否在容器中运行

        Returns:
            是否在容器模式中
        """
        return self._container_mode

    def save_session_id(self, session_id: Optional[str]) -> None:
        """
        保存 session ID 到文件

        Args:
            session_id: session ID，如果为 None 则删除文件
        """
        if session_id:
            self.session_id_file.parent.mkdir(parents=True, exist_ok=True)
            self.session_id_file.write_text(session_id, encoding="utf-8")
            logger.info(f"保存 session ID: {session_id}")
            try:
                payload: Dict[str, Union[str, int]] = {
                    "session_id": session_id,
                    "agent": self.name,
                    "session_scope": self.session_scope,
                    "run_id": (os.environ.get("AGENT_RUN_ID") or "").strip(),
                    "system_type": (os.environ.get("SYSTEM_TYPE") or "").strip(),
                }
                self.session_meta_file.write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            except Exception as e:
                logger.debug(f"写入 session meta 失败: {e}")
        else:
            if self.session_id_file.exists():
                self.session_id_file.unlink()
                logger.info("清除 session ID")
            if self.session_meta_file.exists():
                self.session_meta_file.unlink()
                logger.info("清除 session meta")

    def load_session_id(self) -> Optional[str]:
        """
        从文件加载 session ID

        Returns:
            session ID 或 None
        """
        if self.session_id_file.exists():
            session_id = self.session_id_file.read_text(encoding="utf-8").strip()
            if session_id:
                logger.info(f"加载 session ID: {session_id}")
                return session_id
        return None

    def _resolve_system_type(self) -> str:
        """Resolve system type from config/env with database fallback."""
        return (self.config.get("system_type") or get_env("SYSTEM_TYPE") or "database").strip()

    def _build_sut_for_prompt(self, system_type: str):
        """Create SUT instance used for prompt generation."""
        from sut import create_sut, load_config as load_sut_config

        sut_config = load_sut_config(system_type)
        system_section: Dict[str, Any] = {}
        if hasattr(sut_config, "get"):
            maybe_section = sut_config.get(system_type, {})
            if isinstance(maybe_section, dict):
                system_section = maybe_section
        return create_sut(system_type, self.sut_dir, system_section)

    def _build_fallback_init_prompt(self, system_type: str) -> str:
        """Build robust fallback init prompt when SUT prompt loading fails."""
        normalized = (system_type or "database").strip().lower() or "database"

        if normalized == "database":
            return f"""Build a custom MySQL-like database implementation.

Requirements:
1. Use Python and do not depend on existing database libraries.
2. Implement core MySQL protocol behavior, including Handshake V10, authentication (`mysql_native_password`), at least COM_QUERY + OK/ERR/basic ResultSet, and COM_INIT_DB/COM_PING/COM_QUIT.
3. Must support concurrent connections and basic concurrency control.
4. Implement core SQL commands: CREATE DATABASE, CREATE TABLE, SHOW, INSERT, SELECT, UPDATE, DELETE.
5. Compatibility for benchmark workloads:
   - Support transactions and autocommit (BEGIN/COMMIT/ROLLBACK, SET autocommit=0/1).
   - DDL support for PRIMARY KEY, INDEX/KEY, NOT NULL, DEFAULT, AUTO_INCREMENT.
   - Provide `information_schema` + SHOW introspection (TABLES/COLUMNS/INDEX/CREATE TABLE).
6. Create `start.sh` and read port from `DB_PORT`.
7. Use `./spec/` as reference if available, but validate behavior with runnable local tests.
8. Include PLAN.md with prioritized TODO items and acceptance tests.
"""

        return f"""Build a runnable `{normalized}` implementation in the current directory.

Requirements:
1. Deliver a minimal runnable implementation first (core behavior + start script).
2. Keep code structure extensible for later iterations.
3. Use `./spec/` as reference if available, but validate behavior with runnable local tests.
4. Include PLAN.md with prioritized TODO items and acceptance tests.
"""

    def get_init_prompt(self) -> str:
        """
        获取初始化数据库的提示

        Returns:
            初始化提示字符串
        """
        system_type = self._resolve_system_type()
        try:
            sut = self._build_sut_for_prompt(system_type)
            return sut.get_init_prompt()
        except Exception as e:
            logger.warning(f"Failed to load SUT init prompt for {system_type}, using fallback: {e}")
            return self._build_fallback_init_prompt(system_type or "database")

    def get_improve_prompt(self, iteration: int) -> str:
        """
        获取改进数据库的提示

        Args:
            iteration: 迭代次数

        Returns:
            改进提示字符串
        """
        system_type = self._resolve_system_type()
        try:
            sut = self._build_sut_for_prompt(system_type)
            return sut.get_improve_prompt(iteration)
        except Exception as e:
            logger.warning(f"Failed to load SUT improve prompt for {system_type}, using fallback: {e}")

        brief, brief_file = self._read_latest_brief_summary()
        has_spec = False
        spec_dir = self.sut_dir / "spec"
        if spec_dir.is_dir():
            has_spec = any(
                p.is_file() and not p.name.startswith(".")
                for p in spec_dir.rglob("*")
            )

        prompt = f"""Improve the `{system_type or 'database'}` implementation in the current directory.

This is improvement iteration #{iteration}. Please:
1. Analyze current code, recent test outcomes, and identify one highest-impact issue.
2. Implement one focused improvement while keeping the system runnable.
3. Add or update reproducible local tests, run them, and fix defects based on observed results.
4. Keep changes minimal and iteration-friendly (no large rewrites unless necessary).
"""
        if brief:
            prompt += f"""

5. Benchmark briefs are stored as `./last_brief/last_brief_i.txt`; the latest one is `{brief_file}` (lagging and potentially inaccurate).
Notes:
* The benchmark brief is not updated in real time and may be inconsistent with the current code state.
* Do not treat it as the only source of truth or optimize only for that report.
* Use current code analysis plus reproducible local tests (run by you in this iteration) to diagnose issues and validate fixes.
* If the brief conflicts with your actual test results, trust your actual test results and explain the discrepancy.
* Diagnose, modify code, run tests, and verify fixes based on your own executed test outputs. Build and run your own regression suite. Any conclusion must come from tests executed in this iteration; the brief is only a directional hint.
"""
        if has_spec:
            prompt += """

6. Additional implementation spec docs are available under `./spec/` (reference material).
Notes:
* Treat spec docs like the benchmark brief: useful direction, but potentially stale/incomplete.
* Cross-check spec requirements with current code analysis and reproducible tests run in this iteration.
* If spec text conflicts with your actual test results, trust your actual test results and explain the discrepancy.
"""

        return prompt

    def initialize(self) -> bool:
        """
        Initialize the system - send the agent the init prompt to generate the system.

        Returns:
            True if initialization succeeded
        """
        prompt = self.get_init_prompt()
        logger.info("Starting system initialization...")
        result = self.run_command(prompt, max_retries=self.max_retries)
        self.last_command_result = result
        if result.success:
            logger.info("System initialization completed")
        else:
            logger.error("System initialization failed")

        # Save initialization iteration (iteration 0)
        if self.log_manager:
            session_id = self.load_session_id()
            self.log_manager.save_iteration(
                iteration=0,
                prompt=prompt,
                use_resume=False,
                session_id=session_id,
                result=result
            )

        return result.success

    def improve(self, iteration: int) -> bool:
        """
        Ask the agent to improve the system.

        Args:
            iteration: Iteration number

        Returns:
            True if improvement succeeded
        """
        prompt = self.get_improve_prompt(iteration)
        logger.info(f"Starting improvement iteration #{iteration}...")
        result = self.run_command(
            prompt,
            use_resume=self.iteration_use_resume,
            max_retries=self.max_retries,
        )
        self.last_command_result = result
        if result.success:
            logger.info(f"Improvement iteration #{iteration} completed")
        else:
            logger.warning(f"Improvement iteration #{iteration} failed")

        # Save iteration details
        if self.log_manager:
            session_id = self.load_session_id()
            self.log_manager.save_iteration(
                iteration=iteration,
                prompt=prompt,
                use_resume=self.iteration_use_resume,
                session_id=session_id,
                result=result
            )

        return result.success

    def initialize_database(self) -> bool:
        """
        Initialize the database (backward-compatible wrapper).

        Delegates to :meth:`initialize`.
        """
        return self.initialize()

    def improve_database(self, iteration: int) -> bool:
        """
        Improve the database (backward-compatible wrapper).

        Delegates to :meth:`improve`.
        """
        return self.improve(iteration)
