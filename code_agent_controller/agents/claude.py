"""
Anthropic Claude Code CLI 代理实现
"""

import os
import re
import json
import time
import logging
import subprocess
import shlex
from pathlib import Path
from typing import Optional, Dict, Any

from ..base import CodeAgentBase, is_container_mode, get_container_workdir, CommandResult
from ..utils import get_env, get_env_bool, run_subprocess_streaming

logger = logging.getLogger(__name__)


class ClaudeCodeAgent(CodeAgentBase):
    """
    Anthropic Claude Code CLI 代理实现

    使用 Anthropic 的 Claude Code CLI 工具执行代码生成和改进任务。

    环境变量:
        ANTHROPIC_API_KEY: Anthropic API 密钥（兼容）
        ANTHROPIC_AUTH_TOKEN: Claude Gateway 鉴权令牌
        CLAUDE_PROVIDER: Claude 兼容网关提供商（anthropic/zai/bailian）
        CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS: 是否跳过权限确认
    """

    name = "claude"

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        # Claude Code 在非交互模式下如果不跳过权限确认，往往会拒绝/阻止文件创建与编辑。
        # 在容器模式下，容器边界已经是主要安全隔离，因此默认开启跳过权限确认，
        # 以避免 "所有文件创建命令都被阻止" 的情况。
        self.dangerously_skip_permissions = get_env_bool(
            "CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS", is_container_mode()
        )
        self.model = self._resolve_model(config, "CLAUDE_MODEL", "CODE_AGENT_MODEL")
        provider = (config or {}).get("provider")
        if isinstance(provider, str):
            provider = provider.strip()
        self.provider = provider or get_env("CLAUDE_PROVIDER")
        # Normalize common provider name aliases for backward compatibility
        if self.provider:
            _aliases = {"z.ai": "zai", "dashscope": "bailian"}
            self.provider = _aliases.get(self.provider.lower(), self.provider)

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._registry = ProviderRegistry.get_instance()
            self._resolved = self._registry.resolve_provider(
                "claude", model=self.model, provider_hint=self.provider,
            )
        except Exception:
            self._registry = None
            self._resolved = None

    def _get_completion_pattern(self):
        """Detect ``{"type":"result"}`` in stream-json output."""
        def _is_result_line(line: str) -> bool:
            return '"type":"result"' in line or '"type": "result"' in line
        return _is_result_line

    def check_cli(self) -> bool:
        """检查 claude CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Claude Code CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("Claude Code CLI 未找到。请安装: npm install -g @anthropic-ai/claude-code")
            return False
        except Exception as e:
            logger.error(f"检查 Claude Code CLI 时出错: {e}")
            return False
        return False

    def check_api_key(self) -> bool:
        """检查 Claude 鉴权信息是否已设置。"""
        if self._resolved is not None:
            logger.info(f"Claude 鉴权信息已设置 (via {self._resolved.api_key_source})")
            if self._resolved.base_url:
                logger.info(
                    "已启用 Claude 兼容端点: provider=%s base_url=%s model=%s",
                    self._resolved.provider_name,
                    self._resolved.base_url,
                    self.model,
                )
            return True

        logger.error("未设置 ANTHROPIC_API_KEY 或 ANTHROPIC_AUTH_TOKEN 环境变量")
        logger.info("请设置: export ANTHROPIC_API_KEY='your-api-key'")
        logger.info("或设置: export ANTHROPIC_AUTH_TOKEN='your-api-key'")
        return False

    def _get_cli_model(self) -> Optional[str]:
        """Get the model name for CLI --model flag (stripped of provider prefixes)."""
        if self._resolved and self._resolved.model:
            return self._resolved.model
        if self._registry and self.model:
            return self._registry.normalize_model(self.model)
        return self.model

    def _build_env(self) -> Dict[str, str]:
        """
        构建运行 claude CLI 的环境变量。

        Uses ProviderRegistry for provider resolution, API key mirroring,
        base URL injection, and extra env (API_TIMEOUT_MS etc.).
        """
        if self._resolved:
            env = self._resolved.build_env_dict()
        else:
            env = {**os.environ}
            # Fallback: manual ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN mirroring
            api_key = (env.get("ANTHROPIC_API_KEY") or "").strip()
            auth_token = (env.get("ANTHROPIC_AUTH_TOKEN") or "").strip()
            if api_key and not auth_token:
                env["ANTHROPIC_AUTH_TOKEN"] = api_key
            elif auth_token and not api_key:
                env["ANTHROPIC_API_KEY"] = auth_token

        # Bridge non-Anthropic providers: Claude CLI always needs
        # ANTHROPIC_API_KEY and (optionally) ANTHROPIC_BASE_URL.
        # Providers like moonshot store keys in KIMI_API_KEY / KIMI_BASE_URL,
        # so we map the resolved key/url to ANTHROPIC_* env vars.
        # Force-set (not setdefault) because stale ANTHROPIC_BASE_URL from
        # the shell environment must not override the resolved provider's URL.
        if self._resolved and self._resolved.provider_name != "anthropic":
            env["ANTHROPIC_API_KEY"] = self._resolved.api_key
            env["ANTHROPIC_AUTH_TOKEN"] = self._resolved.api_key
            if self._resolved.base_url:
                env["ANTHROPIC_BASE_URL"] = self._resolved.base_url

        # Claude-specific: set model env vars for the CLI when using a
        # non-default provider (gateway, proxy, or non-anthropic native).
        if self._resolved and self._resolved.provider_name != "anthropic":
            cli_model = self._get_cli_model()
            if cli_model:
                env.setdefault("ANTHROPIC_MODEL", cli_model)
                env.setdefault("ANTHROPIC_DEFAULT_OPUS_MODEL", cli_model)
                env.setdefault("ANTHROPIC_DEFAULT_SONNET_MODEL", cli_model)

        return env

    def _build_base_command(self) -> list:
        """构建基础命令"""
        cmd = ["claude"]
        if self.model:
            cli_model = self._get_cli_model()
            cmd.extend(["--model", cli_model])

        # 流式 JSON 输出，使 pipe 模式下也能实时看到中间过程
        # stream-json 在 --print (pipe) 模式下需要 --verbose
        cmd.extend(["--verbose", "--output-format", "stream-json"])

        if is_container_mode():
            logger.info("Running in container mode, container provides security isolation")
            if self.dangerously_skip_permissions:
                logger.info("Container mode: enable --dangerously-skip-permissions to allow non-interactive edits")
                cmd.append("--dangerously-skip-permissions")
            else:
                logger.warning(
                    "Container mode: CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS=false; "
                    "Claude may block file create/edit without interactive approvals"
                )
        elif self.dangerously_skip_permissions:
            logger.warning("使用 --dangerously-skip-permissions 模式运行 Claude Code")
            cmd.append("--dangerously-skip-permissions")

        # 注意：不使用 --print 参数，因为它会禁用工具调用（如文件写入）
        # Claude Code 会自动以非交互模式运行（通过 stdin）

        return cmd

    def _extract_session_id_from_output(self, output: str) -> Optional[str]:
        """从 Claude 输出中提取 session ID。"""
        try:
            for line in output.split("\n"):
                line = line.strip()
                if line.startswith("{") and ("session" in line.lower() or "id" in line.lower()):
                    try:
                        data = json.loads(line)
                        for key in ["session_id", "sessionId", "session", "id"]:
                            value = data.get(key)
                            if isinstance(value, str) and len(value) >= 8:
                                return value
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass

        patterns = [
            r"session[_\s]*id[:\s]+([a-f0-9-]{8,})",
            r"resume[_\s]*id[:\s]+([a-f0-9-]{8,})",
            r'"session_id"\s*:\s*"([^"]+)"',
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    _TIMEOUT_RESUME_PROMPT = (
        "Your previous session timed out before completion. "
        "Continue from where you left off and complete the current task. "
        "Do NOT re-read files you have already read."
    )

    _TRANSIENT_ERROR_RESUME_PROMPT = (
        "Your previous API call failed due to a transient network/server error. "
        "The session is intact. Continue from where you left off and complete the current task. "
        "Do NOT re-read files you have already read."
    )

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 claude 命令"""
        base_cmd = self._build_base_command()
        should_save_session_id = not use_resume
        current_prompt = prompt

        # Resume 模式支持
        if use_resume:
            session_id = self.load_session_id()
            if session_id:
                logger.info(f"使用 resume 模式，恢复 session: {session_id}")
                base_cmd.extend(["--resume", session_id])
            else:
                logger.info("使用 --continue 恢复最近的会话")
                base_cmd.append("--continue")
                should_save_session_id = True

        # 不添加 prompt 作为命令行参数，而是通过 stdin 传递
        cmd = list(base_cmd)

        # Determine working directory
        if is_container_mode():
            workdir = get_container_workdir()
        else:
            workdir = str(self.sut_dir)
        logger.info(
            "执行 Claude Code 命令: mode=%s run_id=%s session_scope=%s cwd=%s",
            "resume" if use_resume else "new",
            (os.environ.get("AGENT_RUN_ID") or "").strip() or "-",
            getattr(self, "session_scope", "-"),
            workdir,
        )
        env = self._build_env()
        if self._resolved and self._resolved.base_url:
            logger.info(
                "Claude provider=%s model=%s base_url=%s",
                self._resolved.provider_name,
                self._get_cli_model(),
                env.get("ANTHROPIC_BASE_URL", self._resolved.base_url),
            )

        last_stdout = ""
        last_stderr = ""
        last_return_code = -1
        start_time = time.time()

        for attempt in range(max_retries):
            try:
                logger.info(
                    "Claude CLI 开始执行 (attempt=%s/%s): %s",
                    attempt + 1,
                    max_retries,
                    " ".join(shlex.quote(part) for part in cmd),
                )
                result = run_subprocess_streaming(
                    cmd,
                    input_text=current_prompt,
                    timeout=self.command_timeout,
                    cwd=workdir,
                    env=env,
                    logger=logger,
                    log_prefix=f"claude/attempt-{attempt + 1}",
                    completion_pattern=self._get_completion_pattern(),
                    completion_grace_seconds=self.completion_grace_seconds,
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "Claude Code 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s,"
                    " grace_killed=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.grace_killed,
                    result.duration_seconds,
                )
                if result.grace_killed:
                    logger.info("CLI process grace-killed after result output (treated as success)")

                if result.timed_out:
                    logger.warning(f"Claude Code 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    # Try to extract session_id for resume on next attempt
                    if attempt < max_retries - 1:
                        timeout_session_id = self._extract_session_id_from_output(last_stdout)
                        if timeout_session_id:
                            logger.info(
                                "超时但已获取 session ID: %s，下次重试将使用 resume 模式",
                                timeout_session_id,
                            )
                            self.save_session_id(timeout_session_id)
                            cmd = self._build_base_command()
                            cmd.extend(["--resume", timeout_session_id])
                            current_prompt = self._TIMEOUT_RESUME_PROMPT
                            should_save_session_id = True
                        time.sleep(5)
                    continue

                if result.return_code == 0:
                    logger.info("Claude Code 命令执行成功")
                    if self._resolved:
                        self._resolved.report_success()
                    if should_save_session_id:
                        session_id = self._extract_session_id_from_output(f"{last_stdout}\n{last_stderr}")
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
                    logger.warning(
                        "Claude Code 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
                        attempt + 1,
                        max_retries,
                        last_return_code,
                        result.duration_seconds,
                    )
                    if last_stderr:
                        logger.warning("错误输出(stderr):\n%s", self._truncate_for_log(last_stderr))
                    if last_stdout:
                        logger.warning("标准输出(stdout):\n%s", self._truncate_for_log(last_stdout))

                    # --- Prompt too long (context overflow): must start fresh ---
                    # Check this BEFORE transient errors, because transient
                    # detection uses broad substring matching ("500" etc.) that
                    # can false-positive on the large JSON stdout of a
                    # prompt-too-long response.
                    if self._is_prompt_too_long_error(last_stdout or "", last_stderr or ""):
                        logger.warning("Prompt 超长（context overflow），清除 session 并降级执行")
                        self.save_session_id(None)
                        if attempt < max_retries - 1:
                            cmd = self._build_base_command()
                            current_prompt = prompt  # use original prompt, not resume prompt
                            should_save_session_id = True
                            time.sleep(5)
                        continue

                    # --- Transient API/network error: resume the same session ---
                    if self._is_transient_api_error(last_stdout, last_stderr):
                        # Rotate key before retry (e.g. on rate limit 429)
                        if self._resolved:
                            error_reason = self._classify_api_error(last_stdout, last_stderr)
                            if error_reason and self._resolved.report_failure(error_reason):
                                logger.info("临时性错误触发 key 轮换")
                                env = self._build_env()
                        if attempt < max_retries - 1:
                            failed_session_id = self._extract_session_id_from_output(last_stdout)
                            if failed_session_id:
                                logger.info(
                                    "检测到临时性 API/网络错误，保留 session %s，下次重试将使用 resume 模式",
                                    failed_session_id,
                                )
                                self.save_session_id(failed_session_id)
                                cmd = self._build_base_command()
                                cmd.extend(["--resume", failed_session_id])
                                current_prompt = self._TRANSIENT_ERROR_RESUME_PROMPT
                                should_save_session_id = True
                                backoff = min(30, 10 * (attempt + 1))
                                logger.info("临时性错误退避等待 %s 秒后重试...", backoff)
                                time.sleep(backoff)
                                continue
                            else:
                                logger.warning(
                                    "检测到临时性 API/网络错误，但无法提取 session ID，将降级执行"
                                )

                    # --- Non-transient failure on first resume attempt: degrade ---
                    if use_resume and attempt == 0:
                        if self._is_no_previous_session_error(last_stdout, last_stderr):
                            logger.warning("Resume 失败且会话不存在，清除 session 并降级执行")
                            self.save_session_id(None)
                        else:
                            logger.warning("Resume 失败但非会话缺失，保留 session 并降级执行")
                        cmd = self._build_base_command()
                        should_save_session_id = True

                    # Key rotation on API errors
                    if self._resolved:
                        error_reason = self._classify_api_error(last_stdout, last_stderr)
                        if error_reason and self._resolved.report_failure(error_reason):
                            env = self._build_env()

                    if attempt < max_retries - 1:
                        time.sleep(5)

            except Exception as e:
                logger.error(f"执行 Claude Code 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "Claude Code 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
