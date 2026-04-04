"""
Grok CLI 代理实现
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


class GrokCliAgent(CodeAgentBase):
    """
    Grok CLI 代理实现

    使用 X.AI 的 Grok CLI 工具执行代码生成和改进任务。
    Headless 模式自动批准所有操作，不需要单独的审批模式标志。
    不支持 session resume。

    环境变量:
        GROK_API_KEY: Grok API 密钥
        XAI_API_KEY: X.AI API 密钥（备选）
        GROK_MODEL: 模型名称
        GROK_BASE_URL: 可选的 API base URL
    """

    name = "grok"

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        self.model = self._resolve_model(config, "GROK_MODEL", "CODE_AGENT_MODEL")
        base_url = (config or {}).get("base_url")
        if isinstance(base_url, str):
            base_url = base_url.strip()
        self.base_url = base_url or get_env("GROK_BASE_URL")

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._provider = ProviderRegistry.get_instance().resolve_provider(
                "grok", model=self.model,
            )
        except Exception:
            self._provider = None

    def check_cli(self) -> bool:
        """检查 grok CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["grok", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Grok CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("Grok CLI 未找到。请参考官方文档安装")
            return False
        except Exception as e:
            logger.error(f"检查 Grok CLI 时出错: {e}")
            return False
        return False

    def check_api_key(self) -> bool:
        """检查 API 密钥是否已设置"""
        if self._provider is not None:
            logger.info(f"Grok 认证信息已设置 (via {self._provider.api_key_source})")
            return True

        logger.error("未设置 Grok 认证信息：需要 GROK_API_KEY 或 XAI_API_KEY")
        return False

    def _build_base_command(self) -> list:
        """构建基础命令"""
        cmd = ["grok"]
        if self.model:
            cmd.extend(["--model", self.model])
        if self.base_url:
            cmd.extend(["--base-url", self.base_url])
        return cmd

    def _build_env(self) -> Dict[str, str]:
        """构建运行 grok CLI 的环境变量。"""
        if self._provider:
            return self._provider.build_env_dict()
        return {**os.environ}

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 grok 命令

        Grok CLI headless 模式不支持 session resume，use_resume 参数被忽略。
        """
        base_cmd = self._build_base_command()
        cmd = list(base_cmd)

        workdir = self.get_workdir()
        cmd.extend(["--prompt", prompt])
        cmd.extend(["--directory", workdir])

        logger.info(
            "执行 Grok CLI 命令: mode=new run_id=%s session_scope=%s cwd=%s",
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
                    "Grok CLI 开始执行 (attempt=%s/%s): %s",
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
                    log_prefix=f"grok/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "Grok CLI 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.duration_seconds,
                )

                if result.timed_out:
                    logger.warning(f"Grok CLI 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                if result.return_code == 0:
                    logger.info("Grok CLI 命令执行成功")
                    return CommandResult(
                        success=True,
                        stdout=last_stdout,
                        stderr=last_stderr,
                        return_code=last_return_code,
                        duration_seconds=result.duration_seconds
                    )
                else:
                    logger.warning(
                        "Grok CLI 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
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
                logger.error(f"执行 Grok CLI 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "Grok CLI 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
