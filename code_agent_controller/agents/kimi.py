"""
Moonshot Kimi Code CLI 代理实现
"""

import os
import re
import json
import time
import logging
import subprocess
import shlex
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

from ..base import CodeAgentBase, CommandResult
from ..utils import WORK_DIR, get_env, get_config_string, run_subprocess_streaming

logger = logging.getLogger(__name__)


class KimiCodeAgent(CodeAgentBase):
    """
    Moonshot Kimi Code CLI 代理实现

    使用 Kimi Code CLI 工具执行代码生成和改进任务。

    环境变量:
        KIMI_API_KEY: Kimi 官方 API 密钥（推荐）
        MOONSHOT_API_KEY: 兼容别名，会自动映射为 KIMI_API_KEY
        KIMI_MODEL: Kimi 模型名称（例如 kimi-k2.5）
        KIMI_SHARE_DIR: Kimi CLI 状态目录（默认 ~/.kimi）
    """

    name = "kimi"
    _AUTO_PROVIDER_NAME = "auto_provider"
    _DEFAULT_KIMI_BASE_URL = "https://api.moonshot.ai/v1"
    _KIMI_OPEN_PLATFORM_BASE_URLS: Tuple[str, ...] = (
        "https://api.moonshot.ai/v1",
        "https://api.moonshot.cn/v1",
    )
    _DEFAULT_MODEL_MAX_CONTEXT_SIZE = 262144
    _KIMI_MODEL_PREFIXES = ("moonshot-ai/", "moonshot/")
    _RUNTIME_ERROR_PATTERNS: Tuple[Tuple[str, str], ...] = (
        (r"invalid_authentication_error", "invalid_authentication_error"),
        (r"invalid authentication", "invalid_authentication_error"),
        (r"error code:\s*401", "http_401"),
        (r"\bllm not set\b", "llm_not_set"),
    )

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        self.model = get_config_string(config, "model", "KIMI_MODEL", "CODE_AGENT_MODEL")
        self.thinking = self._resolve_thinking_preference(config)
        self.share_dir = self._resolve_share_dir()
        self._auto_base_url_index = 0

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._provider = ProviderRegistry.get_instance().resolve_provider(
                "kimi", model=self.model,
            )
        except Exception:
            self._provider = None

    def _resolve_share_dir(self) -> Path:
        configured = (get_env("KIMI_SHARE_DIR") or "").strip()
        if configured:
            return Path(configured).expanduser()
        return Path.home() / ".kimi"

    def check_cli(self) -> bool:
        """检查 kimi CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["kimi", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                logger.info(f"Kimi CLI 已安装: {(result.stdout or result.stderr).strip()}")
                return True
        except FileNotFoundError:
            logger.error("Kimi CLI 未找到。请参考官方文档安装 Kimi Code CLI")
            return False
        except Exception as e:
            logger.error(f"检查 Kimi CLI 时出错: {e}")
            return False
        return False

    def _has_kimi_config(self) -> bool:
        """检查是否存在可用的 Kimi CLI 配置文件。"""
        config_path = self.share_dir / "config.toml"
        if not config_path.exists():
            return False
        try:
            content = config_path.read_text(encoding="utf-8").strip()
            return bool(content)
        except Exception as e:
            logger.debug(f"读取 Kimi 配置失败: {e}")
            return False

    def check_api_key(self) -> bool:
        """检查 Kimi 鉴权信息是否已设置。"""
        if self._provider is not None:
            logger.info(f"Kimi 认证信息已设置 (via {self._provider.api_key_source})")
            return True
        if self._has_kimi_config():
            logger.info("检测到 Kimi CLI 本地配置，将使用本地配置鉴权")
            return True

        logger.error("未设置 Kimi 鉴权信息")
        logger.info("请设置: export KIMI_API_KEY='your-api-key'（或配置 ~/.kimi/config.toml）")
        return False

    def _build_base_command(self) -> List[str]:
        """构建基础命令。"""
        cmd = ["kimi", "--work-dir", self.get_workdir(), "--print"]
        model_override_config = self._build_model_override_config()
        if model_override_config:
            cmd.extend(["--config", model_override_config])
        if self.thinking is True:
            cmd.append("--thinking")
        elif self.thinking is False:
            cmd.append("--no-thinking")
        if self.model:
            cmd.extend(["--model", self.model])
        return cmd

    @staticmethod
    def _format_command_for_log(cmd: List[str]) -> str:
        """对命令做日志脱敏，避免泄露 --config 里的密钥。"""
        masked: List[str] = []
        skip_next = False
        for idx, part in enumerate(cmd):
            if skip_next:
                skip_next = False
                continue
            if part == "--config" and idx + 1 < len(cmd):
                masked.extend([part, "<redacted-config>"])
                skip_next = True
                continue
            masked.append(part)
        return " ".join(shlex.quote(part) for part in masked)

    @staticmethod
    def _parse_bool(value: Any) -> Optional[bool]:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "t", "yes", "y", "on"}:
                return True
            if normalized in {"0", "false", "f", "no", "n", "off"}:
                return False
        return None

    def _resolve_thinking_preference(self, config: Optional[Dict[str, Any]]) -> Optional[bool]:
        """解析 thinking 偏好。优先级: KIMI_THINKING > 配置项 thinking > 约定默认值。"""
        from_env = self._parse_bool(get_env("KIMI_THINKING"))
        if from_env is not None:
            return from_env

        if isinstance(config, dict):
            from_config = self._parse_bool(config.get("thinking"))
            if from_config is not None:
                return from_config

        normalized_model = self._normalize_kimi_model_name((self.model or "").strip()).lower()
        if normalized_model == "kimi-k2.5":
            return True
        return None

    def _normalize_kimi_model_name(self, model_name: str) -> str:
        """将 OpenRouter/OpenClaw 风格前缀模型名规范化为 Kimi API 可识别的标识。"""
        normalized = model_name.strip()
        lowered = normalized.lower()
        for prefix in self._KIMI_MODEL_PREFIXES:
            if lowered.startswith(prefix):
                return normalized[len(prefix):]
        return normalized

    def _resolve_max_context_size(self) -> int:
        raw = (os.environ.get("KIMI_MODEL_MAX_CONTEXT_SIZE") or "").strip()
        if not raw:
            return self._DEFAULT_MODEL_MAX_CONTEXT_SIZE
        try:
            parsed = int(raw)
        except ValueError:
            logger.warning("无效的 KIMI_MODEL_MAX_CONTEXT_SIZE=%r，回退为默认值 %s", raw, self._DEFAULT_MODEL_MAX_CONTEXT_SIZE)
            return self._DEFAULT_MODEL_MAX_CONTEXT_SIZE
        if parsed <= 0:
            logger.warning("KIMI_MODEL_MAX_CONTEXT_SIZE 必须为正整数，当前=%s，回退为默认值 %s", parsed, self._DEFAULT_MODEL_MAX_CONTEXT_SIZE)
            return self._DEFAULT_MODEL_MAX_CONTEXT_SIZE
        return parsed

    def _resolve_model_capabilities(self) -> List[str]:
        raw = (os.environ.get("KIMI_MODEL_CAPABILITIES") or "").strip()
        capabilities: List[str] = []
        if raw:
            for item in raw.split(","):
                capability = item.strip()
                if capability and capability not in capabilities:
                    capabilities.append(capability)

        if self.thinking is True and "thinking" not in capabilities and "always_thinking" not in capabilities:
            capabilities.append("thinking")
        return capabilities

    def _resolve_provider_for_model_override(self, env: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        根据当前环境变量推断可用 provider，并返回最小配置所需字段。

        优先级:
        1) KIMI_API_KEY / MOONSHOT_API_KEY -> type=kimi
        """
        kimi_key = (env.get("KIMI_API_KEY") or "").strip()
        moonshot_key = (env.get("MOONSHOT_API_KEY") or "").strip()
        kimi_base_url = (env.get("KIMI_BASE_URL") or "").strip()
        explicit_base_url = kimi_base_url

        if kimi_key or moonshot_key:
            if explicit_base_url:
                base_url = explicit_base_url
            else:
                base_url = self._KIMI_OPEN_PLATFORM_BASE_URLS[self._auto_base_url_index]
            return {
                "type": "kimi",
                "base_url": base_url,
                "api_key": kimi_key or moonshot_key,
            }

        return None

    @staticmethod
    def _has_explicit_base_url(env: Dict[str, str]) -> bool:
        # Check os.environ directly: _build_env() may inject the registry's
        # default_base_url as KIMI_BASE_URL which should not block URL rotation.
        return bool((os.environ.get("KIMI_BASE_URL") or "").strip())

    def _try_rotate_kimi_base_url_after_auth_error(self, runtime_error: Optional[str], env: Dict[str, str]) -> bool:
        """
        当未显式指定 base_url 时，认证失败后在 moonshot.ai / moonshot.cn 之间切换一次重试。
        """
        if runtime_error != "invalid_authentication_error":
            return False
        if self._has_explicit_base_url(env):
            return False

        provider = self._resolve_provider_for_model_override(env)
        if not provider or provider.get("type") != "kimi":
            return False

        if self._auto_base_url_index + 1 >= len(self._KIMI_OPEN_PLATFORM_BASE_URLS):
            return False
        self._auto_base_url_index += 1
        return True

    @staticmethod
    def _rebuild_command_with_runtime_flags(base_cmd: List[str], previous_cmd: List[str], prompt: str) -> List[str]:
        """在重建 base_cmd 后，保留 session/continue 标志位并重新附加 prompt。"""
        new_cmd = list(base_cmd)
        if "--session" in previous_cmd:
            session_index = previous_cmd.index("--session")
            if session_index + 1 < len(previous_cmd):
                new_cmd.extend(["--session", previous_cmd[session_index + 1]])
        elif "--continue" in previous_cmd:
            new_cmd.append("--continue")

        new_cmd.extend(["--prompt", prompt])
        return new_cmd

    def _build_model_override_config(self) -> Optional[str]:
        """
        当通过 --model 指定模型时，为 Kimi CLI 自动注入最小可用配置。

        这样即使首次在 Docker 中启动（尚未 /login），也不会出现 "LLM not set"。
        """
        model_name = (self.model or "").strip()
        if not model_name:
            return None

        provider = self._resolve_provider_for_model_override(os.environ)
        if not provider:
            return None
        model_identifier = model_name
        if provider["type"] == "kimi":
            model_identifier = self._normalize_kimi_model_name(model_name)

        model_entry: Dict[str, Any] = {
            "provider": self._AUTO_PROVIDER_NAME,
            "model": model_identifier,
            "max_context_size": self._resolve_max_context_size(),
        }
        capabilities = self._resolve_model_capabilities()
        if capabilities:
            model_entry["capabilities"] = capabilities

        config = {
            "default_model": model_name,
            "default_thinking": bool(self.thinking) if self.thinking is not None else False,
            "providers": {
                self._AUTO_PROVIDER_NAME: {
                    "type": provider["type"],
                    "base_url": provider["base_url"],
                    "api_key": provider["api_key"],
                }
            },
            "models": {
                model_name: model_entry
            },
        }
        return json.dumps(config, ensure_ascii=False, separators=(",", ":"))

    def _detect_runtime_error(self, stdout: str, stderr: str) -> Optional[str]:
        """从 stdout/stderr 中识别 Kimi CLI 语义错误（即使 return_code=0）。"""
        text = f"{stdout}\n{stderr}".lower()
        for pattern, label in self._RUNTIME_ERROR_PATTERNS:
            if re.search(pattern, text):
                return label
        return None

    def _build_env(self) -> Dict[str, str]:
        """构建运行 kimi CLI 的环境变量。"""
        if self._provider:
            env = self._provider.build_env_dict()
        else:
            env = {**os.environ}
        # Ensure KIMI_API_KEY is set from MOONSHOT_API_KEY if needed
        if not (env.get("KIMI_API_KEY") or "").strip():
            moonshot_api_key = (env.get("MOONSHOT_API_KEY") or "").strip()
            if moonshot_api_key:
                env["KIMI_API_KEY"] = moonshot_api_key
        return env

    def _extract_session_id_from_output(self, output: str) -> Optional[str]:
        """从 Kimi CLI 输出中提取 session ID。"""
        try:
            for line in output.split("\n"):
                line = line.strip()
                if not line or not line.startswith("{"):
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for key in ["session_id", "sessionId", "session", "id"]:
                    value = data.get(key)
                    if isinstance(value, str) and len(value.strip()) >= 8:
                        return value.strip()
        except Exception:
            pass

        patterns = [
            r'"session_id"\s*:\s*"([^"]+)"',
            r'"sessionId"\s*:\s*"([^"]+)"',
            r"session[_\s-]*id[:\s]+([a-zA-Z0-9._-]{8,})",
            r"--session\s+([a-zA-Z0-9._-]{8,})",
            r"\b([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\b",
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _list_session_candidates(self) -> List[Tuple[str, float]]:
        """
        从 Kimi share 目录中扫描会话目录，返回 (session_id, mtime) 列表。

        Kimi 默认会将 session 保存在:
        ~/.kimi/sessions/<workdir-hash>/<session-id>/
        """
        sessions_root = self.share_dir / "sessions"
        if not sessions_root.exists():
            return []

        candidates: List[Tuple[str, float]] = []
        for path in sessions_root.glob("*/*"):
            if not path.is_dir():
                continue
            session_id = path.name.strip()
            if len(session_id) < 8:
                continue
            try:
                mtime = path.stat().st_mtime
            except Exception:
                continue
            candidates.append((session_id, mtime))
        candidates.sort(key=lambda item: item[1], reverse=True)
        return candidates

    def _get_latest_session_id(self) -> Optional[str]:
        """从本地 Kimi session 目录推断最近一次会话 ID。"""
        candidates = self._list_session_candidates()
        if not candidates:
            return None
        return candidates[0][0]

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3,
    ) -> CommandResult:
        """运行 kimi 命令"""
        base_cmd = self._build_base_command()
        cmd = list(base_cmd)
        should_save_session_id = not use_resume

        if use_resume:
            session_id = self.load_session_id()
            if session_id:
                logger.info(f"使用 resume 模式，恢复 session: {session_id}")
                cmd.extend(["--session", session_id])
            else:
                logger.info("使用 --continue 恢复最近会话")
                cmd.append("--continue")
                should_save_session_id = True

        cmd.extend(["--prompt", prompt])

        logger.info(
            "执行 Kimi CLI 命令: mode=%s run_id=%s session_scope=%s cwd=%s",
            "resume" if use_resume else "new",
            (os.environ.get("AGENT_RUN_ID") or "").strip() or "-",
            getattr(self, "session_scope", "-"),
            self.get_workdir(),
        )

        last_stdout = ""
        last_stderr = ""
        last_return_code = -1
        start_time = time.time()

        for attempt in range(max_retries):
            try:
                logger.info(
                    "Kimi CLI 开始执行 (attempt=%s/%s): %s",
                    attempt + 1,
                    max_retries,
                    self._format_command_for_log(cmd),
                )
                result = run_subprocess_streaming(
                    cmd,
                    timeout=self.command_timeout,
                    cwd=str(WORK_DIR),
                    env=self._build_env(),
                    logger=logger,
                    log_prefix=f"kimi/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "Kimi CLI 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.duration_seconds,
                )

                if result.timed_out:
                    logger.warning(f"Kimi CLI 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                runtime_error = self._detect_runtime_error(last_stdout, last_stderr)
                if runtime_error:
                    logger.warning(
                        "Kimi CLI 输出包含错误信号，判定执行失败 (attempt=%s/%s, error=%s)",
                        attempt + 1,
                        max_retries,
                        runtime_error,
                    )
                    if result.return_code == 0:
                        last_return_code = 1

                    rotated = self._try_rotate_kimi_base_url_after_auth_error(runtime_error, self._build_env())
                    if rotated:
                        base_cmd = self._build_base_command()
                        cmd = self._rebuild_command_with_runtime_flags(base_cmd, cmd, prompt)
                        logger.warning(
                            "检测到鉴权失败，自动切换 Kimi Open Platform 端点后重试: %s",
                            self._KIMI_OPEN_PLATFORM_BASE_URLS[self._auto_base_url_index],
                        )

                if result.return_code == 0 and not runtime_error:
                    logger.info("Kimi CLI 命令执行成功")
                    if self._provider:
                        self._provider.report_success()
                    if should_save_session_id:
                        session_id = self._extract_session_id_from_output(f"{last_stdout}\n{last_stderr}")
                        if not session_id:
                            session_id = self._get_latest_session_id()
                        if session_id:
                            self.save_session_id(session_id)
                    return CommandResult(
                        success=True,
                        stdout=last_stdout,
                        stderr=last_stderr,
                        return_code=last_return_code,
                        duration_seconds=result.duration_seconds,
                    )

                logger.warning(
                    "Kimi CLI 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.duration_seconds,
                )
                if last_stderr:
                    logger.warning("错误输出(stderr):\n%s", self._truncate_for_log(last_stderr))
                if last_stdout:
                    logger.warning("标准输出(stdout):\n%s", self._truncate_for_log(last_stdout))

                if use_resume and attempt == 0:
                    if self._is_no_previous_session_error(last_stdout, last_stderr):
                        logger.warning("Resume 失败且会话不存在，清除 session 并降级执行")
                        self.save_session_id(None)
                    elif self._is_prompt_too_long_error(last_stdout or "", last_stderr or ""):
                        logger.warning("Prompt 超长（context overflow），清除 session 并降级执行")
                        self.save_session_id(None)
                    else:
                        logger.warning("Resume 失败但非会话缺失，保留 session 并降级执行")
                    should_save_session_id = True
                    cmd = list(base_cmd)
                    cmd.extend(["--prompt", prompt])

                # Key rotation on API errors (env rebuilt per attempt)
                if self._provider:
                    error_reason = self._classify_api_error(last_stdout, last_stderr)
                    if error_reason:
                        self._provider.report_failure(error_reason)

                if attempt < max_retries - 1:
                    time.sleep(5)

            except Exception as e:
                logger.error(f"执行 Kimi CLI 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "Kimi CLI 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration,
        )
