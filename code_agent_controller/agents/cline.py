"""
Cline CLI 代理实现
"""

import os
import time
import logging
import subprocess
import shlex
from pathlib import Path
from typing import Optional, Dict, Any, List

from ..base import CodeAgentBase, CommandResult
from ..utils import ensure_directory, get_env, get_env_bool, run_subprocess_streaming

logger = logging.getLogger(__name__)


class ClineAgent(CodeAgentBase):
    """
    Cline CLI 代理实现

    使用 Cline CLI 工具执行代码生成和改进任务。
    使用 -y (yolo/autonomous) 模式进行非交互式执行。
    不支持 session resume。

    环境变量:
        CLINE_API_KEY: Cline API 密钥（通用优先级最高）
        CLINE_BASE_URL: Cline OpenAI Compatible base URL 覆盖
        DASHSCOPE_API_KEY: 百炼/Coding Plan API Key
        OPENAI_API_KEY: OpenAI/OpenAI Compatible 备选 API 密钥
        ANTHROPIC_API_KEY: Anthropic 备选 API 密钥
        CLINE_MODEL: 模型名称（支持 bailian-coding-plan/* 前缀）
        CLINE_PROVIDER: LLM 提供商 (anthropic, openai, bailian, dashscope 等)
    """

    name = "cline"

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        self.model = self._resolve_model(config, "CLINE_MODEL", "CODE_AGENT_MODEL")
        provider = (config or {}).get("provider")
        if isinstance(provider, str):
            provider = provider.strip()
        self.provider = provider or get_env("CLINE_PROVIDER")
        # Normalize common provider name aliases for backward compatibility
        if self.provider:
            _aliases = {
                "dashscope": "bailian",
                "openai-compatible": "openai",
                "openai_compatible": "openai",
                "claude": "anthropic",
            }
            self.provider = _aliases.get(self.provider.lower(), self.provider)
        self.verbose_output = get_env_bool("CLINE_VERBOSE", True)
        self.json_output = get_env_bool("CLINE_JSON_OUTPUT", True)

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._registry = ProviderRegistry.get_instance()
            self._resolved = self._registry.resolve_provider(
                "cline", model=self.model, provider_hint=self.provider,
            )
        except Exception:
            self._registry = None
            self._resolved = None

    def _get_runtime_model(self) -> str:
        """Get model name for CLI (stripped of provider prefixes)."""
        if self._resolved and self._resolved.model:
            return self._resolved.model
        model = (self.model or "").strip()
        if self._registry:
            return self._registry.normalize_model(model)
        return model

    def _get_cline_auth_provider(self) -> Optional[str]:
        """Determine the cline auth provider type ('anthropic' or 'openai')."""
        if self._resolved:
            return "anthropic" if self._resolved.api_type == "anthropic" else "openai"
        return None

    def _get_default_config_dir(self, env: Dict[str, str]) -> Path:
        home_dir = Path((env.get("HOME") or str(Path.home()))).expanduser()
        return home_dir / ".cline" / "data"

    def _get_managed_config_dir(self) -> Path:
        return self.session_id_file.parent / "cline_data"

    def _should_bootstrap_auth(self, env: Dict[str, str]) -> bool:
        return self._resolved is not None

    def _resolve_config_dir(self, env: Dict[str, str]) -> Optional[Path]:
        explicit = (env.get("CLINE_DIR") or "").strip()
        if explicit:
            return Path(explicit).expanduser()
        if self._should_bootstrap_auth(env):
            return self._get_managed_config_dir()
        return self._get_default_config_dir(env)

    def _has_existing_auth_config(self, env: Dict[str, str]) -> bool:
        config_dir = self._resolve_config_dir(env)
        if not config_dir:
            return False
        return (config_dir / "secrets.json").exists()

    def check_cli(self) -> bool:
        """检查 cline CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["cline", "version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Cline CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("Cline CLI 未找到。请运行 npm install -g cline 安装")
            return False
        except Exception as e:
            logger.error(f"检查 Cline CLI 时出错: {e}")
            return False
        return False

    def check_api_key(self) -> bool:
        """检查 API 密钥是否已设置"""
        if self._resolved is not None:
            logger.info(f"Cline 认证信息已设置 (via {self._resolved.api_key_source})")
            return True
        env = self._build_env()
        if self._has_existing_auth_config(env):
            logger.info("Cline 认证信息已设置 (via %s)", self._resolve_config_dir(env) / "secrets.json")
            return True

        logger.error("未设置 Cline 认证信息：需要 CLINE_API_KEY、DASHSCOPE_API_KEY、OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
        return False

    def _build_cline_prefix(self, env: Dict[str, str]) -> List[str]:
        cmd = ["cline"]
        config_dir = self._resolve_config_dir(env)
        if config_dir:
            cmd.extend(["--config", str(config_dir)])
        return cmd

    def _build_base_command(self, env: Dict[str, str]) -> List[str]:
        """构建基础命令"""
        cmd = self._build_cline_prefix(env)
        cmd.append("-y")
        model = self._get_runtime_model()
        if model:
            cmd.extend(["--model", model])
        if self.verbose_output:
            cmd.append("--verbose")
        if self.json_output:
            cmd.append("--json")
        return cmd

    def _build_env(self) -> Dict[str, str]:
        """构建运行 cline CLI 的环境变量。"""
        env = {**os.environ}
        if self._should_bootstrap_auth(env):
            config_dir = self._resolve_config_dir(env)
            if config_dir is not None:
                ensure_directory(config_dir)
                env["CLINE_DIR"] = str(config_dir)
        return env

    def _build_auth_command(self, env: Dict[str, str]) -> Optional[List[str]]:
        if not self._resolved:
            return None

        auth_provider = self._get_cline_auth_provider()
        if not auth_provider:
            return None

        cmd = self._build_cline_prefix(env)
        cmd.append("auth")
        cmd.extend(["--provider", auth_provider, "-k", self._resolved.api_key])

        model = self._get_runtime_model()
        if model:
            cmd.extend(["--modelid", model])

        # Only pass --baseurl for OpenAI-compatible providers;
        # Cline CLI rejects --baseurl for the native Anthropic provider.
        if auth_provider == "openai" and self._resolved.base_url:
            cmd.extend(["--baseurl", self._resolved.base_url])

        return cmd

    # Map internal registry names to user-friendly display names for logging
    _DISPLAY_PROVIDER_MAP = {
        "bailian_openai_gateway": "bailian",
        "bailian_claude_gateway": "bailian",
        "zai_gateway": "zai",
    }

    def _log_runtime_configuration(self, env: Dict[str, str], workdir: str) -> None:
        raw_name = self._resolved.provider_name if self._resolved else "auto"
        provider_name = self.provider or self._DISPLAY_PROVIDER_MAP.get(raw_name, raw_name)
        auth_provider = self._get_cline_auth_provider() or "auto"
        base_url = (self._resolved.base_url if self._resolved else None) or "-"
        config_dir = self._resolve_config_dir(env)
        logger.info(
            "Cline runtime config: task_provider=%s auth_provider=%s model=%s base_url=%s config_dir=%s cwd=%s verbose=%s json=%s",
            provider_name,
            auth_provider,
            self._get_runtime_model() or "-",
            base_url,
            str(config_dir) if config_dir else "-",
            workdir,
            self.verbose_output,
            self.json_output,
        )

    def _format_command_for_log(self, cmd: List[str]) -> str:
        masked_cmd: List[str] = []
        redact_next = False
        for part in cmd:
            if redact_next:
                masked_cmd.append("***")
                redact_next = False
                continue
            masked_cmd.append(part)
            if part in {"--key", "--apikey", "-k"}:
                redact_next = True
        return " ".join(shlex.quote(part) for part in masked_cmd)

    def _bootstrap_auth(self, env: Dict[str, str]) -> Optional[str]:
        auth_cmd = self._build_auth_command(env)
        if not auth_cmd:
            return None

        logger.info("同步 Cline 认证配置: %s", self._format_command_for_log(auth_cmd))
        result = subprocess.run(
            auth_cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        if result.returncode == 0:
            if stdout:
                logger.info("Cline auth stdout:\n%s", self._truncate_for_log(stdout))
            if stderr:
                logger.warning("Cline auth stderr:\n%s", self._truncate_for_log(stderr))
            return None

        if stderr:
            logger.error("Cline auth stderr:\n%s", self._truncate_for_log(stderr))
        if stdout:
            logger.error("Cline auth stdout:\n%s", self._truncate_for_log(stdout))
        return stderr or stdout or "cline auth failed"

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 cline 命令

        Cline CLI 不支持 session resume，use_resume 参数被忽略。
        """
        env = self._build_env()
        auth_error = self._bootstrap_auth(env)
        if auth_error:
            return CommandResult(
                success=False,
                stdout="",
                stderr=auth_error,
                return_code=-1,
                duration_seconds=0.0,
            )

        base_cmd = self._build_base_command(env)
        cmd = list(base_cmd)

        workdir = self.get_workdir()
        cmd.extend(["--cwd", workdir, prompt])
        self._log_runtime_configuration(env, workdir)

        logger.info(
            "执行 Cline CLI 命令: mode=new run_id=%s session_scope=%s cwd=%s",
            (os.environ.get("AGENT_RUN_ID") or "").strip() or "-",
            getattr(self, "session_scope", "-"),
            workdir,
        )

        last_stdout = ""
        last_stderr = ""
        last_return_code = -1
        start_time = time.time()

        for attempt in range(max_retries):
            try:
                logger.info(
                    "Cline CLI 开始执行 (attempt=%s/%s): %s",
                    attempt + 1,
                    max_retries,
                    self._format_command_for_log(cmd),
                )
                result = run_subprocess_streaming(
                    cmd,
                    timeout=self.command_timeout,
                    cwd=workdir,
                    env=env,
                    logger=logger,
                    log_prefix=f"cline/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "Cline CLI 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.duration_seconds,
                )

                if result.timed_out:
                    logger.warning(f"Cline CLI 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                if result.return_code == 0:
                    logger.info("Cline CLI 命令执行成功")
                    return CommandResult(
                        success=True,
                        stdout=last_stdout,
                        stderr=last_stderr,
                        return_code=last_return_code,
                        duration_seconds=result.duration_seconds
                    )
                else:
                    logger.warning(
                        "Cline CLI 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
                        attempt + 1,
                        max_retries,
                        last_return_code,
                        result.duration_seconds,
                    )
                    if last_stderr:
                        logger.warning("错误输出(stderr):\n%s", self._truncate_for_log(last_stderr))
                    if last_stdout:
                        logger.warning("标准输出(stdout):\n%s", self._truncate_for_log(last_stdout))

                    if attempt < max_retries - 1:
                        time.sleep(5)

            except Exception as e:
                logger.error(f"执行 Cline CLI 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "Cline CLI 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
