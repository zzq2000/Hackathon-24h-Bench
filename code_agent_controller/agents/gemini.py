"""
Google Gemini CLI 代理实现
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
from ..utils import get_env, run_subprocess_streaming

logger = logging.getLogger(__name__)


class GeminiCliAgent(CodeAgentBase):
    """
    Google Gemini CLI 代理实现

    使用 Google 的 Gemini CLI 工具执行代码生成和改进任务。

    环境变量:
        GEMINI_API_KEY: Google API 密钥
        GEMINI_SANDBOX_MODE: 是否启用 Gemini CLI 沙箱 (none/false/0 关闭；其他值开启)
        GEMINI_APPROVAL_MODE: Gemini CLI 审批模式 (default/auto_edit/yolo)。容器模式默认 yolo。
    """

    name = "gemini"

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        self.sandbox_mode = get_env("GEMINI_SANDBOX_MODE", "none")
        approval_mode = (config or {}).get("approval_mode")
        if isinstance(approval_mode, str):
            approval_mode = approval_mode.strip()
        self.approval_mode = approval_mode or get_env("GEMINI_APPROVAL_MODE")
        self.model = self._resolve_model(config, "GEMINI_MODEL", "CODE_AGENT_MODEL")

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._provider = ProviderRegistry.get_instance().resolve_provider(
                "gemini", model=self.model,
            )
        except Exception:
            self._provider = None

    def check_cli(self) -> bool:
        """检查 gemini CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Gemini CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("Gemini CLI 未找到。请参考官方文档安装")
            return False
        except Exception as e:
            logger.error(f"检查 Gemini CLI 时出错: {e}")
            return False
        return False

    def check_api_key(self) -> bool:
        """检查 Google API 密钥是否已设置"""
        if self._provider is not None:
            logger.info(f"Gemini 认证信息已设置 (via {self._provider.api_key_source})")
            return True

        logger.error("未设置 Gemini 认证信息：需要 GEMINI_API_KEY 或 GOOGLE_GENAI_USE_VERTEXAI/GOOGLE_GENAI_USE_GCA")
        logger.info("请设置: export GEMINI_API_KEY='your-api-key'（或使用 Vertex/GCA 认证方式）")
        return False

    def _build_base_command(self) -> list:
        """构建基础命令"""
        cmd = ["gemini"]
        if self.model:
            cmd.extend(["--model", self.model])

        # 默认在容器模式下启用 yolo，避免停留在“plan/等待批准”而不执行文件编辑
        approval_mode = (self.approval_mode or "").strip()
        if not approval_mode and is_container_mode():
            approval_mode = "yolo"
        if approval_mode:
            cmd.extend(["--approval-mode", approval_mode])

        # 设置沙箱模式（当前 gemini CLI 中 --sandbox 为布尔开关，不接受 "basic/strict" 等值）
        sandbox_mode = (self.sandbox_mode or "").strip().lower()
        if sandbox_mode and sandbox_mode not in {"none", "false", "0", "off"}:
            if sandbox_mode not in {"true", "1", "on"}:
                logger.warning(
                    f"GEMINI_SANDBOX_MODE={self.sandbox_mode!r} 将按开启处理；"
                    "当前 gemini CLI 的 --sandbox 不支持模式值"
                )
            cmd.append("--sandbox")

        cmd.extend(["--output-format", "stream-json"])

        return cmd

    def _extract_session_id_from_output(self, output: str) -> Optional[str]:
        """从 gemini CLI 输出中提取 session ID

        Gemini CLI 的 session ID 格式为 UUID (例如: 21885a08-f462-410b-a28e-787dccf9cde0)
        """
        # 尝试从 JSON 输出中提取 (如果使用 --output-format json)
        try:
            for line in output.split('\n'):
                line = line.strip()
                if line.startswith('{') and ('session' in line.lower() or 'id' in line.lower()):
                    try:
                        data = json.loads(line)
                        for key in ['session_id', 'sessionId', 'session', 'id']:
                            if key in data:
                                value = data[key]
                                if isinstance(value, str) and len(value) > 10:
                                    return value
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass

        # 尝试从文本输出中提取 UUID 格式的 session ID
        # Gemini 使用标准 UUID 格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        patterns = [
            # Standard UUID format
            r"session[_\s]*(?:id)?[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r"Session[_\s]*(?:ID)?[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            # JSON format
            r'"session_id"\s*:\s*"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
            r'"sessionId"\s*:\s*"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
            # Bracketed format from --list-sessions output
            r'\[([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\]',
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _get_latest_session_id(self, cwd: Optional[str] = None) -> Optional[str]:
        """通过 --list-sessions 获取最新的 session ID"""
        try:
            workdir = cwd or self.get_workdir()
            result = subprocess.run(
                ["gemini", "--list-sessions"],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=workdir,
                env=self._build_env()
            )
            if result.returncode == 0 and result.stdout:
                # 解析 --list-sessions 输出，提取第一个（最新的）session ID
                # 格式: "  1. 标题 (X days ago) [uuid]"
                session_id = self._extract_session_id_from_output(result.stdout)
                if session_id:
                    logger.info(f"从 --list-sessions 获取到最新 session ID: {session_id}")
                    return session_id
        except Exception as e:
            logger.debug(f"获取 session 列表时出错: {e}")
        return None

    def _build_env(self) -> Dict[str, str]:
        """构建运行 gemini CLI 的环境变量。"""
        if self._provider:
            return self._provider.build_env_dict()
        return {**os.environ}

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 gemini 命令"""
        base_cmd = self._build_base_command()
        cmd = list(base_cmd)
        should_save_session_id = not use_resume

        # Resume 模式支持
        if use_resume:
            session_id = self.load_session_id()
            if session_id:
                logger.info(f"使用 resume 模式，恢复 session: {session_id}")
                cmd.extend(["--resume", session_id])
            else:
                # 类似 Claude 的 --continue，Gemini 支持 --resume latest
                logger.info("使用 --resume latest 恢复最近的会话")
                cmd.extend(["--resume", "latest"])
                # 如果之前没有可恢复的 session ID，则在成功后保存实际 session ID
                should_save_session_id = True

        # 添加提示
        # gemini CLI 支持使用 --prompt（已标记 deprecated 但仍可用）来执行 one-shot
        cmd.extend(["--prompt", prompt])

        # Determine working directory
        workdir = self.get_workdir()
        logger.info(
            "执行 Gemini CLI 命令: mode=%s run_id=%s session_scope=%s cwd=%s",
            "resume" if use_resume else "new",
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
                    "Gemini CLI 开始执行 (attempt=%s/%s): %s",
                    attempt + 1,
                    max_retries,
                    " ".join(shlex.quote(part) for part in cmd),
                )
                result = run_subprocess_streaming(
                    cmd,
                    timeout=self.command_timeout,
                    cwd=workdir,
                    env=self._build_env(),
                    logger=logger,
                    log_prefix=f"gemini/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "Gemini CLI 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.duration_seconds,
                )

                if result.timed_out:
                    logger.warning(f"Gemini CLI 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                if result.return_code == 0:
                    logger.info("Gemini CLI 命令执行成功")
                    # if last_stdout:
                    #     logger.info(f"输出: {last_stdout}")

                    # 提取并保存 session ID 以便后续 resume
                    if should_save_session_id:
                        # 首先尝试从输出中提取
                        session_id = self._extract_session_id_from_output(last_stdout)
                        if not session_id:
                            # 如果输出中没有，尝试通过 --list-sessions 获取最新的
                            session_id = self._get_latest_session_id(cwd=workdir)
                        if session_id:
                            logger.info(f"保存 session ID: {session_id}")
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
                        "Gemini CLI 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
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
                        else:
                            logger.warning("Resume 失败但非会话缺失，保留 session 并降级执行")
                        should_save_session_id = True
                        cmd = list(base_cmd)
                        cmd.extend(["--prompt", prompt])

                    if attempt < max_retries - 1:
                        time.sleep(5)

            except Exception as e:
                logger.error(f"执行 Gemini CLI 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "Gemini CLI 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
