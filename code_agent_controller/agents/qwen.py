"""
Qwen Code 代理实现
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


class QwenCodeAgent(CodeAgentBase):
    """
    Qwen Code 代理实现

    使用阿里巴巴的 Qwen Code CLI 工具执行代码生成和改进任务。

    环境变量:
        QWEN_API_KEY: Qwen API 密钥
        DASHSCOPE_API_KEY: DashScope API 密钥
        QWEN_MODEL: 模型名称
        QWEN_APPROVAL_MODE: 审批模式 (plan/default/auto-edit/yolo)。容器模式默认 yolo。
    """

    name = "qwen"

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        approval_mode = (config or {}).get("approval_mode")
        if isinstance(approval_mode, str):
            approval_mode = approval_mode.strip()
        self.approval_mode = approval_mode or get_env("QWEN_APPROVAL_MODE")
        self.model = self._resolve_model(config, "QWEN_MODEL", "CODE_AGENT_MODEL")

        # Resolve provider via registry
        try:
            from ..providers import ProviderRegistry
            self._provider = ProviderRegistry.get_instance().resolve_provider(
                "qwen", model=self.model,
            )
        except Exception:
            self._provider = None

    def check_cli(self) -> bool:
        """检查 qwen CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["qwen", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Qwen CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("Qwen CLI 未找到。请参考官方文档安装")
            return False
        except Exception as e:
            logger.error(f"检查 Qwen CLI 时出错: {e}")
            return False
        return False

    def check_api_key(self) -> bool:
        """检查 API 密钥是否已设置"""
        if self._provider is not None:
            logger.info(f"Qwen 认证信息已设置 (via {self._provider.api_key_source})")
            return True

        # 也接受 ~/.qwen/settings.json 中的 OAuth 配置
        settings_file = Path.home() / ".qwen" / "settings.json"
        if settings_file.exists():
            try:
                data = json.loads(settings_file.read_text())
                if data.get("auth") or data.get("oauth") or data.get("token"):
                    logger.info("Qwen 认证信息已设置 (via ~/.qwen/settings.json)")
                    return True
            except Exception:
                pass

        logger.error("未设置 Qwen 认证信息：需要 QWEN_API_KEY, DASHSCOPE_API_KEY, OPENAI_API_KEY 或 ~/.qwen/settings.json")
        return False

    def _build_base_command(self) -> list:
        """构建基础命令"""
        cmd = ["qwen"]
        if self.model:
            cmd.extend(["--model", self.model])

        # 默认在容器模式下启用 yolo，避免停留在等待批准
        approval_mode = (self.approval_mode or "").strip()
        if not approval_mode and is_container_mode():
            approval_mode = "yolo"
        if approval_mode:
            cmd.extend(["--approval-mode", approval_mode])

        cmd.extend(["--output-format", "stream-json"])

        return cmd

    def _extract_session_id_from_output(self, output: str) -> Optional[str]:
        """从 qwen CLI 输出中提取 session ID

        Qwen 可能在输出中包含 --resume <session-id> 提示
        """
        # 尝试从 JSON 输出中提取
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

        # 尝试从文本中提取 --resume <session-id> 提示
        patterns = [
            r"--resume\s+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r"session[_\s]*(?:id)?[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r"Session[_\s]*(?:ID)?[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r'"session_id"\s*:\s*"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
            # Also match non-UUID session IDs from --resume hints
            r"--resume\s+(\S{8,})",
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _build_env(self) -> Dict[str, str]:
        """构建运行 qwen CLI 的环境变量。"""
        if self._provider:
            return self._provider.build_env_dict()
        return {**os.environ}

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 qwen 命令"""
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
                logger.info("使用 --continue 恢复最近的会话")
                cmd.append("--continue")
                should_save_session_id = True

        # 添加提示
        cmd.extend(["-p", prompt])

        workdir = self.get_workdir()
        logger.info(
            "执行 Qwen CLI 命令: mode=%s run_id=%s session_scope=%s cwd=%s",
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
                    "Qwen CLI 开始执行 (attempt=%s/%s): %s",
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
                    log_prefix=f"qwen/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "Qwen CLI 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.duration_seconds,
                )

                if result.timed_out:
                    logger.warning(f"Qwen CLI 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                if result.return_code == 0:
                    logger.info("Qwen CLI 命令执行成功")

                    if should_save_session_id:
                        session_id = self._extract_session_id_from_output(last_stdout)
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
                        "Qwen CLI 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
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
                        cmd.extend(["-p", prompt])

                    if attempt < max_retries - 1:
                        time.sleep(5)

            except Exception as e:
                logger.error(f"执行 Qwen CLI 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "Qwen CLI 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
