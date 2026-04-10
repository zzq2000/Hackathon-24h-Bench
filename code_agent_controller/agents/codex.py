"""
OpenAI Codex CLI 代理实现
"""

import os
import re
import json
import time
import logging
import subprocess
import shlex
import textwrap
from pathlib import Path
from typing import Optional, Dict, Any

from ..base import CodeAgentBase, is_container_mode, get_container_workdir, CommandResult
from ..utils import WORK_DIR, get_env, get_env_bool, get_config_string, run_subprocess_streaming

logger = logging.getLogger(__name__)


class CodexAgent(CodeAgentBase):
    """
    OpenAI Codex CLI 代理实现

    使用 OpenAI 的 Codex CLI 工具执行代码生成和改进任务。

    环境变量:
        OPENAI_API_KEY: OpenAI API 密钥
        CODEX_USE_DOCKER: 是否使用 Docker 模式运行
        CODEX_DOCKER_IMAGE: Docker 镜像名称
        CODEX_DOCKER_CONTAINER_NAME: Docker 容器名称
        CODEX_BYPASS_SANDBOX: 是否绕过沙箱限制
    """

    name = "codex"
    _DEFAULT_LOG_MAX_CHARS = -1  # 默认不限制日志输出长度

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)

        # Codex 特定配置
        self.use_docker = get_env_bool("CODEX_USE_DOCKER", False)
        self.docker_image = get_env("CODEX_DOCKER_IMAGE", "codex-env")
        self.docker_container_name = get_env("CODEX_DOCKER_CONTAINER_NAME", "codex-executor")
        self.bypass_sandbox = get_env_bool("CODEX_BYPASS_SANDBOX", False)
        self.container_sut_dir = f"/workspace/{(config or {}).get('system_type', 'database')}"
        self.model = get_config_string(config, "model", "CODEX_MODEL", "CODE_AGENT_MODEL")

        # Provider hint: explicit provider selection (e.g. "litellm", "openrouter")
        provider = (config or {}).get("provider")
        if isinstance(provider, str):
            provider = provider.strip()
        self.provider = provider or get_env("CODEX_PROVIDER")

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._provider = ProviderRegistry.get_instance().resolve_provider(
                "codex", model=self.model, provider_hint=self.provider,
            )
        except Exception:
            self._provider = None

        # 沙箱权限配置
        self.sandbox_permissions = [
            "network-access",
            "socket-access",
            "unix-socket-access",
            "bind-socket",
            "create-socket"
        ]

    def check_cli(self) -> bool:
        """检查 codex-cli 是否已安装"""
        try:
            result = subprocess.run(
                ["codex", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Codex CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("Codex CLI 未找到。请安装: npm install -g @openai/codex")
            return False
        except Exception as e:
            logger.error(f"检查 Codex CLI 时出错: {e}")
            return False
        return False

    def _get_model_from_codex_config(self) -> Optional[str]:
        """Read the default model from ~/.codex/config.toml if present."""
        config_path = Path.home() / ".codex" / "config.toml"
        if not config_path.exists():
            return None
        try:
            for line in config_path.read_text().splitlines():
                stripped = line.strip()
                # Match top-level 'model = "..."' (before any [section] header)
                if stripped.startswith("model") and "=" in stripped:
                    _, _, value = stripped.partition("=")
                    return value.strip().strip('"').strip("'")
        except Exception as e:
            logger.debug(f"Error reading model from codex config: {e}")
        return None

    # -- config.toml management ------------------------------------------------

    def _get_codex_config_path(self) -> Path:
        """Return the path to the Codex CLI config.toml."""
        return Path.home() / ".codex" / "config.toml"

    def _has_custom_codex_config(self) -> bool:
        """Check if a custom Codex CLI config.toml with a non-default provider exists."""
        config_path = self._get_codex_config_path()
        if not config_path.exists():
            return False
        try:
            content = config_path.read_text()
            if "model_providers" in content:
                return True
        except Exception as e:
            logger.debug(f"Error reading codex config: {e}")
        return False

    def _is_proxy_mode(self) -> bool:
        """Whether the resolved provider is a proxy (LiteLLM, OpenRouter, etc.).

        Proxy mode requires a config.toml with custom ``model_providers``
        because Codex CLI reads ``base_url`` from config, not from env vars.
        Native mode uses ``codex login`` instead.
        """
        return bool(self._provider and self._provider.is_proxy)

    def _resolve_wire_api(self) -> str:
        """Determine the wire_api for Codex CLI config.toml.

        - ``CODEX_WIRE_API`` env var takes highest priority.
        - For proxy providers the default is ``responses`` (OpenAI
          Responses API) which is broadly supported by modern proxies
          (OpenRouter, LiteLLM ≥1.40).  Override to ``chat`` if your
          proxy only supports Chat Completions.
        """
        explicit = get_env("CODEX_WIRE_API")
        if explicit and explicit.strip().lower() in ("responses", "chat"):
            return explicit.strip().lower()
        return "responses"

    def _generate_codex_config(self) -> str:
        """Generate config.toml content for proxy-mode providers.

        Creates a ``[model_providers.wrapper]`` section that points Codex
        CLI to the proxy's base_url and reads the API key from the correct
        env var.
        """
        model = self.model or "gpt-4o"
        base_url = self._provider.base_url if self._provider else "http://localhost:4000"
        env_key = self._provider.api_key_source if self._provider else "OPENAI_API_KEY"
        wire_api = self._resolve_wire_api()

        return textwrap.dedent(f"""\
            model = "{model}"
            model_provider = "wrapper"
            stream_idle_timeout_ms = 300000

            web_search = "disabled"

            [sandbox_workspace_write]
            network_access = true

            [model_providers.wrapper]
            name = "wrapper"
            base_url = "{base_url}"
            wire_api = "{wire_api}"
            env_key = "{env_key}"
        """)

    def _ensure_proxy_config(self) -> None:
        """Write or update config.toml for proxy-mode providers.

        If a config.toml already exists, patch only ``base_url`` and
        ``env_key`` to preserve user customizations (profiles, sandbox
        settings, etc.).  Otherwise generate a fresh config.
        """
        if not self._provider:
            return

        config_path = self._get_codex_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)

        if config_path.exists() and self._has_custom_codex_config():
            # Patch existing config in-place
            self._patch_codex_config(config_path)
        else:
            # Generate fresh config for proxy mode
            config_path.write_text(self._generate_codex_config())
            logger.info(
                "Generated Codex config.toml for proxy provider %s at %s",
                self._provider.provider_name,
                config_path,
            )

    def _patch_codex_config(self, config_path: Path) -> None:
        """Patch an existing config.toml's base_url, env_key, and wire_api."""
        try:
            content = config_path.read_text()
            original = content

            if self._provider.base_url:
                content = re.sub(
                    r'(base_url\s*=\s*)"[^"]*"',
                    rf'\1"{self._provider.base_url}"',
                    content,
                )
            if self._provider.api_key_source:
                content = re.sub(
                    r'(env_key\s*=\s*)"[^"]*"',
                    rf'\1"{self._provider.api_key_source}"',
                    content,
                )
            wire_api = self._resolve_wire_api()
            content = re.sub(
                r'(wire_api\s*=\s*)"[^"]*"',
                rf'\1"{wire_api}"',
                content,
            )

            if content != original:
                config_path.write_text(content)
                logger.info(
                    "Patched Codex config.toml: base_url=%s env_key=%s",
                    self._provider.base_url or "(unchanged)",
                    self._provider.api_key_source or "(unchanged)",
                )
        except Exception as e:
            logger.warning(f"Failed to patch Codex config.toml: {e}")

    def _remove_custom_provider_from_config(self) -> None:
        """Strip ``model_provider`` and ``[model_providers.*]`` from config.toml.

        Called in native mode so Codex CLI uses its built-in OpenAI
        provider instead of a stale wrapper section left from a previous
        proxy run.
        """
        config_path = self._get_codex_config_path()
        if not config_path.exists():
            return
        try:
            content = config_path.read_text()
            if "model_providers" not in content:
                return
            # Remove top-level model_provider = "wrapper"
            content = re.sub(r'^model_provider\s*=\s*"[^"]*"\n?', '', content, flags=re.MULTILINE)
            # Remove [model_providers.*] sections and their contents
            content = re.sub(
                r'^\[model_providers\.[^\]]*\]\n(?:(?!\[)[^\n]*\n)*',
                '', content, flags=re.MULTILINE,
            )
            config_path.write_text(content)
            logger.info("Removed custom model_providers from config.toml for native mode")
        except Exception as e:
            logger.debug(f"Error cleaning config.toml for native mode: {e}")

    # -- env / auth ------------------------------------------------------------

    def _build_env(self) -> Dict[str, str]:
        """Build environment for Codex CLI subprocess."""
        if self._provider:
            return self._provider.build_env_dict()
        return {**os.environ}

    def check_api_key(self) -> bool:
        """检查 API 密钥和认证配置。

        Three provider modes:
        1. **Native** (openai): ``codex login --with-api-key``, no config.toml
           custom provider needed.
        2. **Proxy** (litellm / openrouter / ...): generate or patch
           config.toml with proxy's ``base_url`` and ``env_key``, skip login.
        3. **Legacy** (no provider resolved, existing config.toml): use
           config.toml as-is.
        """
        if self._provider:
            if self._is_proxy_mode():
                # -- Proxy mode: config.toml drives auth -----------------------
                self._ensure_proxy_config()
                logger.info(
                    "Codex proxy mode: provider=%s base_url=%s env_key=%s",
                    self._provider.provider_name,
                    self._provider.base_url,
                    self._provider.api_key_source,
                )
                return True

            # -- Native mode: codex login + ensure no stale wrapper -----------
            self._remove_custom_provider_from_config()
            logger.info(f"OpenAI API 密钥已设置 (via {self._provider.api_key_source})")

            if self._is_logged_in():
                logger.info("Codex CLI 已登录")
                return True

            logger.info("正在使用 API 密钥登录 Codex CLI...")
            if self._login_with_api_key(self._provider.api_key):
                logger.info("Codex CLI 登录成功")
                return True
            else:
                logger.error("Codex CLI 登录失败")
                return False

        # -- Legacy mode: no provider resolved ---------------------------------
        if self._has_custom_codex_config():
            logger.info("Custom Codex CLI config found (legacy mode), skipping API key login")
            return True

        logger.error("未设置 OPENAI_API_KEY 环境变量")
        logger.info("请设置: export OPENAI_API_KEY='your-api-key'")
        return False

    def _is_logged_in(self) -> bool:
        """检查 Codex CLI 是否已登录"""
        try:
            result = subprocess.run(
                ["codex", "login", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            # Login status returns 0 if logged in
            return result.returncode == 0 and "Logged in" in result.stdout
        except Exception as e:
            logger.debug(f"检查登录状态时出错: {e}")
            return False

    def _login_with_api_key(self, api_key: str) -> bool:
        """使用 API 密钥登录 Codex CLI"""
        try:
            # Use echo to pipe the API key to codex login
            result = subprocess.run(
                ["codex", "login", "--with-api-key"],
                input=api_key,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True
            else:
                logger.error(f"登录失败: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"登录时出错: {e}")
            return False

    def get_workdir(self) -> str:
        """获取 codex 实际工作目录"""
        return self.container_sut_dir if self.use_docker else str(self.sut_dir)

    def _extract_session_id_from_output(self, output: str) -> Optional[str]:
        """从 codex 输出中提取 session ID"""
        # 尝试从 JSON 输出中提取
        try:
            for line in output.split('\n'):
                line = line.strip()
                if line.startswith('{') and ('session' in line.lower() or 'thread' in line.lower()):
                    try:
                        data = json.loads(line)
                        for key in ['session_id', 'sessionId', 'session', 'id', 'thread_id', 'threadId']:
                            if key in data:
                                value = data[key]
                                if isinstance(value, str) and len(value) > 10:
                                    return value
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass

        # 尝试从文本输出中提取 session ID
        patterns = [
            r"session[_\s]*id[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r"session[_\s]*id[:\s]+([a-zA-Z0-9_-]{20,})",
            r"Session[_\s]*ID[:\s]+([a-f0-9-]{36})",
            r'"session_id"\s*:\s*"([^"]+)"',
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _build_base_command(self) -> list:
        """构建基础命令"""
        permissions_str = "[" + ", ".join(f'"{p}"' for p in self.sandbox_permissions) + "]"

        # Determine working directory
        if is_container_mode():
            # In container mode the Docker container itself is the security
            # boundary.  Codex's built-in bwrap sandbox requires unprivileged
            # user namespaces which are not reliably available inside
            # containers, so we bypass it here.
            workdir = get_container_workdir()
            cmd = [
                "codex", "exec",
                "--json",
                "--dangerously-bypass-approvals-and-sandbox",
                "--cd", workdir,
                "--skip-git-repo-check",
            ]
            logger.info("Running in container mode, bypassing Codex sandbox (container provides isolation)")
        elif self.bypass_sandbox:
            # Host mode with bypass (legacy, not recommended)
            logger.warning("使用危险模式运行 Codex，绕过沙箱限制")
            cmd = [
                "codex", "exec",
                "--json",
                "--dangerously-bypass-approvals-and-sandbox",
                "--cd", str(self.sut_dir),
                "--skip-git-repo-check",
            ]
        else:
            # Host mode with standard sandbox
            cmd = [
                "codex", "exec",
                "--json",
                "--sandbox", "workspace-write",
                "--cd", str(self.sut_dir),
                "--skip-git-repo-check",
                "--full-auto",
                "-c", f"sandbox_permissions={permissions_str}",
            ]
        # 禁用联网搜索，防止 agent 从网络搜索答案
        cmd.extend(["-c", 'web_search="disabled"'])

        # Determine model: explicit controller model takes priority, then config.toml
        model_to_use = self.model
        if not model_to_use and self._has_custom_codex_config():
            model_to_use = self._get_model_from_codex_config()
            if model_to_use:
                logger.info(f"Using model from codex config.toml: {model_to_use}")
        if model_to_use:
            cmd.extend(["--model", model_to_use])
        return cmd

    def _log_attempt_failure(
        self,
        attempt: int,
        max_retries: int,
        return_code: int,
        duration: float,
        stdout_text: str,
        stderr_text: str,
    ) -> None:
        """Emit detailed but bounded failure logs for a Codex attempt."""
        logger.warning(
            "Codex 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
            attempt + 1,
            max_retries,
            return_code,
            duration,
        )

        clipped_stdout = self._truncate_for_log(stdout_text or "")
        clipped_stderr = self._truncate_for_log(stderr_text or "")

        if clipped_stdout:
            logger.warning("标准输出(stdout):\n%s", clipped_stdout)
        if clipped_stderr:
            logger.warning("错误输出(stderr):\n%s", clipped_stderr)

        combined = f"{stdout_text}\n{stderr_text}".lower()
        if (
            "response.failed" in combined
            or "stream disconnected before completion" in combined
            or "connecting..." in combined
        ):
            logger.warning(
                "检测到流式连接异常特征（response.failed/stream disconnected）。"
                "这通常发生在代理层或上游模型连接不稳定时（例如 LiteLLM 链路）。"
            )

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 codex 命令"""
        env = self._build_env()
        base_cmd = self._build_base_command()
        cmd = list(base_cmd)
        should_save_session_id = not use_resume

        if use_resume:
            session_id = self.load_session_id()
            if session_id:
                logger.info(f"使用 resume 模式，恢复 session: {session_id}")
                cmd.extend(["resume", session_id, prompt])
            else:
                logger.info("未找到本地 session ID，改为直接执行并在成功后保存新 session")
                cmd.append(prompt)
                should_save_session_id = True
        else:
            cmd.append(prompt)

        logger.info(
            "执行 Codex 命令: mode=%s run_id=%s session_scope=%s cwd=%s",
            "resume" if use_resume else "new",
            (os.environ.get("AGENT_RUN_ID") or "").strip() or "-",
            getattr(self, "session_scope", "-"),
            str(self.sut_dir),
        )

        last_stdout = ""
        last_stderr = ""
        last_return_code = -1
        start_time = time.time()

        for attempt in range(max_retries):
            try:
                logger.info(
                    "Codex CLI 开始执行 (attempt=%s/%s): %s",
                    attempt + 1,
                    max_retries,
                    " ".join(shlex.quote(part) for part in cmd),
                )

                result = run_subprocess_streaming(
                    cmd,
                    cwd=str(WORK_DIR),
                    env=env,
                    timeout=self.command_timeout,
                    logger=logger,
                    log_prefix=f"codex/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code

                if result.timed_out:
                    logger.warning(f"Codex 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                if result.return_code == 0:
                    logger.info("Codex 命令执行成功")
                    if self._provider:
                        self._provider.report_success()

                    if should_save_session_id:
                        session_id = self._extract_session_id_from_output(last_stdout)
                        if session_id:
                            self.save_session_id(session_id)

                    return CommandResult(
                        success=True,
                        stdout=last_stdout,
                        stderr=last_stderr,
                        return_code=last_return_code,
                        duration_seconds=result.duration_seconds
                    )
                else:
                    self._log_attempt_failure(
                        attempt=attempt,
                        max_retries=max_retries,
                        return_code=last_return_code,
                        duration=result.duration_seconds,
                        stdout_text=last_stdout,
                        stderr_text=last_stderr,
                    )

                    if use_resume and attempt == 0:
                        if self._is_no_previous_session_error(last_stdout, last_stderr):
                            logger.warning("当前项目无可恢复会话，自动降级为新会话执行")
                            self.save_session_id(None)
                        elif self._is_prompt_too_long_error(last_stdout or "", last_stderr or ""):
                            logger.warning("Prompt 超长（context overflow），清除 session 并降级执行")
                            self.save_session_id(None)
                        else:
                            logger.warning("Resume 失败但非会话缺失，保留 session ID 并降级执行")
                        cmd = base_cmd.copy()
                        cmd.append(prompt)
                        should_save_session_id = True

                    # Key rotation on API errors
                    if self._provider:
                        error_reason = self._classify_api_error(last_stdout, last_stderr)
                        if error_reason and self._provider.report_failure(error_reason):
                            env = self._build_env()

                    if attempt < max_retries - 1:
                        time.sleep(5)

            except Exception as e:
                logger.error(f"执行 Codex 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error("Codex 命令执行失败，已达到最大重试次数")
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
