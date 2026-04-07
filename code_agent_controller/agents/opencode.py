"""
OpenCode 代理实现
"""

import os
import re
import json
import time
import logging
import subprocess
import shlex
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

from ..base import CodeAgentBase, is_container_mode, get_container_workdir, CommandResult
from ..utils import get_env, get_config_int, run_subprocess_streaming

logger = logging.getLogger(__name__)

_BAILIAN_PROVIDER = "bailian-coding-plan"
_BAILIAN_MODEL_PREFIX = f"{_BAILIAN_PROVIDER}/"

# Mapping from ProviderRegistry provider names to OpenCode CLI provider IDs.
# OpenCode CLI (via Vercel AI SDK) natively supports built-in providers that
# auto-read their standard env vars.  Custom providers need opencode.json config.
_REGISTRY_TO_OPENCODE_ID: Dict[str, str] = {
    # Built-in providers — auto-read standard env vars, no config needed
    "openai": "openai",
    "anthropic": "anthropic",
    "google": "google",
    "xai": "xai",
    "openrouter": "openrouter",
    # Custom providers — require opencode.json configuration
    "bailian_claude_gateway": "bailian-coding-plan",
}

# Built-in OpenCode providers that need NO opencode.json config and
# NO OPENCODE_API_KEY bridging — each reads its own env var.
_OPENCODE_BUILTIN_PROVIDERS = frozenset({
    "openai", "anthropic", "google", "xai", "openrouter",
})

# AI SDK npm package for each api_type when generating opencode.json
# for non-built-in providers.
_API_TYPE_TO_SDK_NPM = {
    "anthropic": "@ai-sdk/anthropic",
    "openai": "@ai-sdk/openai-compatible",
    "google": "@ai-sdk/google",
}


def _get_registry():
    """Get the ProviderRegistry instance, or None if unavailable."""
    try:
        from ..providers import ProviderRegistry
        return ProviderRegistry.get_instance()
    except Exception:
        return None


def normalize_opencode_model(model_name: Optional[str]) -> Optional[str]:
    """Normalize user-facing OpenCode model names.

    For Bailian models, keep the canonical bare model name so logs/run-id/session
    scope match other agents such as Claude/Cline.
    """
    if not model_name:
        return None

    normalized = model_name.strip()
    if not normalized:
        return None

    registry = _get_registry()
    if registry:
        return registry.normalize_model(normalized)

    # Fallback: manual prefix stripping
    if normalized.lower().startswith(_BAILIAN_MODEL_PREFIX):
        return normalized[len(_BAILIAN_MODEL_PREFIX):]
    return normalized


def resolve_opencode_runtime_model(model_name: Optional[str]) -> Optional[str]:
    """Resolve the provider/model string required by the OpenCode CLI.

    OpenCode CLI uses ``provider_id/model_name`` format.  Built-in provider
    prefixes (``openai/``, ``anthropic/``, ``google/``, ``xai/``, ``openrouter/``)
    are supported natively via Vercel AI SDK.  Custom providers like
    ``bailian-coding-plan/`` are configured via ``opencode.json``.

    This function handles Bailian model auto-prefixing.  For other bare model
    names, the prefix is added later in ``__init__`` based on the resolved
    ProviderRegistry provider.
    """
    normalized = normalize_opencode_model(model_name)
    if not normalized:
        return None

    if "/" in normalized:
        return normalized

    registry = _get_registry()
    if registry and registry.is_bailian_model(normalized):
        return f"{_BAILIAN_PROVIDER}/{normalized}"

    # Bare model — prefix will be added in __init__ based on resolved provider.
    return normalized


class OpenCodeAgent(CodeAgentBase):
    """
    OpenCode 代理实现

    使用 anomalyco 的 OpenCode CLI 工具执行代码生成和改进任务。
    OpenCode CLI 通过 Vercel AI SDK 支持 75+ 内置 provider，每个 provider
    读取各自的标准环境变量（ANTHROPIC_API_KEY, OPENAI_API_KEY 等）。
    自定义 provider（如百炼网关、LiteLLM）通过 opencode.json 配置。

    环境变量:
        OPENAI_API_KEY / ANTHROPIC_API_KEY / ...: 各 provider 对应的标准 API key
        OPENCODE_MODEL: 模型名称（支持 `provider/model` 格式和 `bailian-coding-plan/*`）
        OPENCODE_APPROVAL_MODE: 审批模式 (build/plan)。容器模式默认 build。
    """

    name = "opencode"
    # OpenCode already enables auto compaction by default. Keep proactive
    # session rotation opt-in so resume paths preserve context unless compaction
    # actually fails and we have to fallback to a new session.
    _DEFAULT_RESUME_TURN_LIMIT = 0
    _CONTEXT_OVERFLOW_PATTERNS = (
        "contextoverflowerror",
        "payload too large",
        "exceeded limit on max bytes to request body",
        "range of input length should be",
        "input length should be",
        "context length exceeded",
        "context window",
    )

    def __init__(self, sut_dir: Path, config: Optional[Dict[str, Any]] = None):
        super().__init__(sut_dir, config)
        approval_mode = (config or {}).get("approval_mode")
        if isinstance(approval_mode, str):
            approval_mode = approval_mode.strip()
        self.approval_mode = approval_mode or get_env("OPENCODE_APPROVAL_MODE")
        raw_model = (config or {}).get("model")
        if isinstance(raw_model, str):
            raw_model = raw_model.strip()
        raw_model = raw_model or get_env("OPENCODE_MODEL") or get_env("CODE_AGENT_MODEL")
        self.original_model = raw_model
        self.model = normalize_opencode_model(raw_model)
        self.runtime_model = resolve_opencode_runtime_model(raw_model)

        # Resolve provider via registry
        provider_hint = (config or {}).get("provider")
        if isinstance(provider_hint, str):
            provider_hint = provider_hint.strip() or None
        try:
            from ..providers import ProviderRegistry
            self._provider = ProviderRegistry.get_instance().resolve_provider(
                "opencode", model=self.model, provider_hint=provider_hint,
            )
        except Exception:
            self._provider = None

        # Determine the OpenCode CLI provider ID from the resolved provider.
        self._opencode_provider_id = self._resolve_opencode_provider_id()

        # OpenCode CLI requires --model in "provider_id/model_name" format.
        # Bailian models are already prefixed by resolve_opencode_runtime_model().
        # For other bare models, add the provider prefix based on the resolved
        # provider (e.g., "anthropic/claude-...", "google/gemini-...").
        if self.runtime_model and "/" not in self.runtime_model:
            if self._opencode_provider_id:
                self.runtime_model = f"{self._opencode_provider_id}/{self.runtime_model}"

        # Generate opencode.json for non-built-in providers (litellm, vllm, etc.)
        self._ensure_custom_provider_config()

        self.resume_turn_limit = get_config_int(
            self.config,
            "resume_turn_limit",
            "OPENCODE_RESUME_TURN_LIMIT",
            default=self._DEFAULT_RESUME_TURN_LIMIT,
        )
        if self.resume_turn_limit < 0:
            logger.warning("resume_turn_limit=%s 非法，回退为 %s", self.resume_turn_limit, self._DEFAULT_RESUME_TURN_LIMIT)
            self.resume_turn_limit = self._DEFAULT_RESUME_TURN_LIMIT
        if self.model and self.original_model and self.model != self.original_model:
            logger.info("OpenCode 模型已规范化: %s -> %s", self.original_model, self.model)
        if self.runtime_model and self.runtime_model != self.model:
            logger.info("OpenCode 运行时模型映射: %s -> %s", self.model, self.runtime_model)

    def check_cli(self) -> bool:
        """检查 opencode CLI 是否已安装"""
        try:
            result = subprocess.run(
                ["opencode", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"OpenCode CLI 已安装: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.error("OpenCode CLI 未找到。请参考官方文档安装")
            return False
        except Exception as e:
            logger.error(f"检查 OpenCode CLI 时出错: {e}")
            return False
        return False

    def check_api_key(self) -> bool:
        """检查 API 密钥是否已设置（支持多种 provider）"""
        if self._provider is not None:
            logger.info(f"OpenCode 认证信息已设置 (via {self._provider.api_key_source})")
            return True
        # Fallback: OPENCODE_API_KEY is agent-specific and not in the provider registry
        opencode_key = get_env("OPENCODE_API_KEY")
        if opencode_key:
            logger.info("OpenCode 认证信息已设置 (via OPENCODE_API_KEY)")
            return True

        logger.error("未设置 OpenCode 认证信息：需要 OPENCODE_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, XAI_API_KEY 或 OPENROUTER_API_KEY")
        return False

    def _build_base_command(self) -> list:
        """构建基础命令"""
        cmd = ["opencode", "run"]
        if self.runtime_model:
            cmd.extend(["--model", self.runtime_model])

        # 默认在容器模式下启用 build agent，避免停留在 plan 模式
        approval_mode = (self.approval_mode or "").strip()
        if not approval_mode and is_container_mode():
            approval_mode = "build"
        if approval_mode:
            cmd.extend(["--agent", approval_mode])

        cmd.extend(["--format", "json"])

        return cmd

    def _extract_session_id_from_output(self, output: str) -> Optional[str]:
        """从 opencode CLI 输出中提取 session ID

        OpenCode 的 session ID 格式为 UUID
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

        # 尝试从文本输出中提取 UUID 格式的 session ID
        patterns = [
            r"session[_\s]*(?:id)?[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r"Session[_\s]*(?:ID)?[:\s]+([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            r'"session_id"\s*:\s*"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
            r'"sessionId"\s*:\s*"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})"',
        ]
        for pattern in patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                return match.group(1)
        return None

    def _build_env(self) -> Dict[str, str]:
        """构建运行 opencode CLI 的环境变量。

        Each built-in OpenCode provider reads its own standard env var
        (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.) automatically via the
        Vercel AI SDK.  No OPENCODE_API_KEY bridging is needed — that env
        var is specific to the "OpenCode Zen" service.

        Custom providers configured in opencode.json use ``{env:VAR}``
        references to read API keys at runtime.

        For built-in providers, inherited base URL env vars (e.g.
        ANTHROPIC_BASE_URL from a different agent config) are stripped so
        the SDK uses its default endpoint.  Without this, a stale
        ANTHROPIC_BASE_URL pointing to OpenRouter / Bailian would silently
        break native Anthropic calls.
        """
        if self._provider:
            env = self._provider.build_env_dict()
            # Built-in OpenCode providers have correct SDK defaults for
            # their API endpoints.  Remove any inherited base URL env var
            # that might redirect requests to a completely different
            # service (e.g. ANTHROPIC_BASE_URL=https://openrouter.ai/api
            # leaking from host env).
            if (self._opencode_provider_id in _OPENCODE_BUILTIN_PROVIDERS
                    and self._provider.base_url_env_key):
                inherited_url = env.pop(self._provider.base_url_env_key, None)
                if inherited_url:
                    logger.info(
                        "Cleared inherited %s=%s for built-in OpenCode "
                        "provider '%s' (SDK will use its default endpoint)",
                        self._provider.base_url_env_key,
                        inherited_url,
                        self._opencode_provider_id,
                    )
        else:
            env = {**os.environ}
        # Map GEMINI_API_KEY to GOOGLE_GENERATIVE_AI_API_KEY for @ai-sdk/google
        if not env.get("GOOGLE_GENERATIVE_AI_API_KEY"):
            for src_key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                val = env.get(src_key)
                if val:
                    env["GOOGLE_GENERATIVE_AI_API_KEY"] = val
                    break
        return env

    # ------------------------------------------------------------------
    # OpenCode provider helpers
    # ------------------------------------------------------------------

    def _resolve_opencode_provider_id(self) -> Optional[str]:
        """Map the resolved ProviderRegistry provider to an OpenCode CLI provider ID.

        Built-in providers have a direct 1:1 mapping (e.g. ``anthropic`` →
        ``anthropic``).  Unmapped providers get a sanitised ID derived from
        the provider name (e.g. ``azure_openai`` → ``azure-openai``).
        """
        if not self._provider:
            return None
        provider_name = self._provider.provider_name
        opencode_id = _REGISTRY_TO_OPENCODE_ID.get(provider_name)
        if opencode_id:
            return opencode_id
        # Derive an ID for unmapped providers (litellm, vllm, sglang, etc.)
        return provider_name.replace("_", "-")

    def _ensure_custom_provider_config(self) -> None:
        """Generate opencode.json entries for non-built-in providers.

        Built-in OpenCode providers (openai, anthropic, google, xai,
        openrouter) read their standard env vars automatically and need no
        config file.  Custom providers require an ``opencode.json`` entry
        with the appropriate ``@ai-sdk/*`` npm package, ``baseURL``, and
        ``apiKey``.

        If the config file already contains an entry for this provider ID
        (e.g. copied from ``third_party/bailian/opencode.json`` in Docker),
        the existing entry is preserved — it may contain model-specific
        options (thinking, modalities) that we should not overwrite.
        """
        if not self._provider or not self._opencode_provider_id:
            return
        opencode_id = self._opencode_provider_id
        if opencode_id in _OPENCODE_BUILTIN_PROVIDERS:
            return

        config_dir = self._get_opencode_config_dir()
        config_file = config_dir / "config.json"

        # Load existing config
        existing: Dict[str, Any] = {}
        if config_file.exists():
            try:
                existing = json.loads(config_file.read_text(encoding="utf-8"))
            except Exception as e:
                logger.debug("Failed to load existing opencode config: %s", e)

        # Need a base_url for non-built-in providers
        base_url = self._provider.base_url
        if not base_url:
            logger.warning(
                "Cannot generate opencode.json for provider %s: no base_url. "
                "Configure it via env var or providers.yaml default_base_url.",
                opencode_id,
            )
            return

        # Determine SDK package from api_type
        api_type = self._provider.api_type
        npm = _API_TYPE_TO_SDK_NPM.get(api_type, "@ai-sdk/openai-compatible")

        # If the provider already exists (e.g. copied from static template in
        # Docker), preserve model capabilities (thinking, modalities) but
        # always refresh connection options from the provider registry so that
        # hardcoded apiKey / baseURL values in the template are overridden.
        if "provider" not in existing:
            existing["provider"] = {}
        prev = existing["provider"].get(opencode_id)

        provider_entry: Dict[str, Any] = {
            "npm": npm,
            "name": opencode_id,
            "options": {
                "baseURL": base_url,
                # {env:VAR} lets OpenCode read the key at runtime
                "apiKey": f"{{env:{self._provider.api_key_source}}}",
            },
        }

        if prev:
            # Preserve model definitions with capabilities from static config
            if "models" in prev:
                provider_entry["models"] = prev["models"]
            logger.info(
                "OpenCode provider %s: refreshed connection options from provider registry",
                opencode_id,
            )
        else:
            logger.info(
                "Generated OpenCode config for provider %s at %s",
                opencode_id, config_file,
            )

        # Register the specific model being used (if not already present)
        if self.model:
            if "models" not in provider_entry:
                provider_entry["models"] = {}
            provider_entry["models"].setdefault(
                self.model, {"name": self.model},
            )

        # Merge into config
        if "$schema" not in existing:
            existing["$schema"] = "https://opencode.ai/config.json"
        existing["provider"][opencode_id] = provider_entry

        # Write config
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file.write_text(
                json.dumps(existing, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning("Failed to write opencode config: %s", e)

    @staticmethod
    def _get_opencode_config_dir() -> Path:
        """Get the OpenCode configuration directory."""
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            return Path(xdg_config) / "opencode"
        return Path.home() / ".config" / "opencode"

    def _load_session_meta(self) -> Dict[str, Any]:
        """Load the persisted session metadata if available."""
        if not self.session_meta_file.exists():
            return {}
        try:
            raw = self.session_meta_file.read_text(encoding="utf-8").strip()
        except Exception as e:
            logger.debug("读取 session meta 失败: %s", e)
            return {}
        if not raw:
            return {}
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            logger.debug("解析 session meta 失败: %s", e)
            return {}
        return payload if isinstance(payload, dict) else {}

    def _write_session_meta(self, payload: Dict[str, Any]) -> None:
        """Persist extended session metadata for OpenCode rotation heuristics."""
        try:
            self.session_meta_file.parent.mkdir(parents=True, exist_ok=True)
            self.session_meta_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except Exception as e:
            logger.debug("写入扩展 session meta 失败: %s", e)

    @staticmethod
    def _coerce_non_negative_int(value: Any) -> int:
        try:
            result = int(value)
        except (TypeError, ValueError):
            return 0
        return max(result, 0)

    def _build_prompt_command(
        self,
        base_cmd: list,
        workdir: str,
        prompt: str,
        *,
        use_resume: bool,
    ) -> Tuple[list, bool, str]:
        """Build the OpenCode command for either a fresh or resumed session."""
        cmd = list(base_cmd)
        cmd.extend(["--dir", workdir])
        should_save_session_id = not use_resume
        session_mode = "new"

        if use_resume:
            session_id = self.load_session_id()
            if session_id:
                logger.info("使用 resume 模式，恢复 session: %s", session_id)
                cmd.extend(["--session", session_id])
                session_mode = "resume"
            else:
                logger.info("使用 --continue 恢复最近的会话")
                cmd.append("--continue")
                should_save_session_id = True
                session_mode = "continue"

        cmd.extend(["--message", prompt])
        return cmd, should_save_session_id, session_mode

    def _get_session_turns(self, session_id: Optional[str]) -> int:
        if not session_id:
            return 0
        payload = self._load_session_meta()
        if payload.get("session_id") != session_id:
            return 0
        return self._coerce_non_negative_int(payload.get("session_turns"))

    def _should_rotate_session_before_resume(self) -> bool:
        """Optional guardrail for deployments that want forced session rotation."""
        if self.resume_turn_limit <= 0:
            return False
        session_id = self.load_session_id()
        if not session_id:
            return False
        turns = self._get_session_turns(session_id)
        if turns < self.resume_turn_limit:
            return False
        logger.warning(
            "OpenCode session turn 数达到阈值 (%s >= %s)，本次改为新会话执行",
            turns,
            self.resume_turn_limit,
        )
        return True

    def _record_session_turn(self, session_id: str, session_mode: str) -> None:
        """Track successful turns for the active OpenCode session."""
        payload = self._load_session_meta()
        turns = 0
        if payload.get("session_id") == session_id:
            turns = self._coerce_non_negative_int(payload.get("session_turns"))
        payload.update(
            {
                "session_id": session_id,
                "agent": self.name,
                "session_scope": self.session_scope,
                "run_id": (os.environ.get("AGENT_RUN_ID") or "").strip(),
                "system_type": (os.environ.get("SYSTEM_TYPE") or "").strip(),
                "session_turns": turns + 1,
                "last_mode": session_mode,
                "last_used_at": int(time.time()),
            }
        )
        self._write_session_meta(payload)

    @staticmethod
    def _extract_json_runtime_error(text: str) -> Dict[str, str]:
        """Extract OpenCode JSON error events from stdout/stderr."""
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(payload.get("type") or "").lower() != "error":
                continue
            error = payload.get("error")
            if isinstance(error, dict):
                name = str(error.get("name") or error.get("type") or "").strip()
                message = str(error.get("message") or error.get("error") or "").strip()
            elif error is None:
                name = ""
                message = ""
            else:
                name = ""
                message = str(error).strip()
            if name or message:
                return {"name": name, "message": message}
        return {}

    def _detect_runtime_error(self, stdout: str, stderr: str) -> Optional[str]:
        """Detect semantic failures even when OpenCode exits with return_code=0."""
        details = self._extract_json_runtime_error(f"{stdout}\n{stderr}")
        # Context overflow detection: only search stderr and extracted error
        # details — NOT the full stdout which contains the agent's own text
        # output (e.g. "413 Payload Too Large") that can cause false positives.
        error_text = "\n".join(
            part for part in (stderr, details.get("name", ""), details.get("message", "")) if part
        ).lower()
        if error_text.strip() and any(pattern in error_text for pattern in self._CONTEXT_OVERFLOW_PATTERNS):
            return "context_overflow"
        if self._is_no_previous_session_error(stdout, stderr):
            return "no_previous_session"
        if details.get("name"):
            return details["name"]
        search_text = "\n".join(
            part for part in (stdout, stderr) if part
        ).lower()
        if search_text.strip() and ('"type":"error"' in search_text or '"type": "error"' in search_text):
            return "runtime_error"
        return None

    def run_command(
        self,
        prompt: str,
        use_resume: bool = False,
        max_retries: int = 3
    ) -> CommandResult:
        """运行 opencode 命令"""
        base_cmd = self._build_base_command()
        workdir = self.get_workdir()
        effective_use_resume = use_resume
        if effective_use_resume and self._should_rotate_session_before_resume():
            self.save_session_id(None)
            effective_use_resume = False
        cmd, should_save_session_id, session_mode = self._build_prompt_command(
            base_cmd,
            workdir,
            prompt,
            use_resume=effective_use_resume,
        )

        logger.info(
            "执行 OpenCode CLI 命令: mode=%s run_id=%s session_scope=%s cwd=%s",
            "resume" if effective_use_resume else "new",
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
                    "OpenCode CLI 开始执行 (attempt=%s/%s): %s",
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
                    log_prefix=f"opencode/attempt-{attempt + 1}",
                )

                last_stdout = result.stdout or ""
                last_stderr = result.stderr or ""
                last_return_code = result.return_code
                logger.info(
                    "OpenCode CLI 尝试结束 (attempt=%s/%s, return_code=%s, timed_out=%s, duration=%.2fs)",
                    attempt + 1,
                    max_retries,
                    last_return_code,
                    result.timed_out,
                    result.duration_seconds,
                )

                if result.timed_out:
                    logger.warning(f"OpenCode CLI 命令超时 (尝试 {attempt + 1}/{max_retries})")
                    last_stderr = last_stderr or "命令执行超时"
                    last_return_code = -1
                    if attempt < max_retries - 1:
                        time.sleep(5)
                    continue

                runtime_error = self._detect_runtime_error(last_stdout, last_stderr)
                if runtime_error:
                    logger.warning(
                        "OpenCode CLI 输出包含错误信号，判定执行失败 (attempt=%s/%s, error=%s)",
                        attempt + 1,
                        max_retries,
                        runtime_error,
                    )
                    if last_return_code == 0:
                        last_return_code = 1

                if result.return_code == 0 and not runtime_error:
                    logger.info("OpenCode CLI 命令执行成功")
                    if self._provider:
                        self._provider.report_success()

                    active_session_id = None
                    combined_output = f"{last_stdout}\n{last_stderr}"
                    if should_save_session_id:
                        active_session_id = self._extract_session_id_from_output(combined_output)
                        if active_session_id:
                            logger.info(f"保存 session ID: {active_session_id}")
                            self.save_session_id(active_session_id)
                    if not active_session_id and effective_use_resume:
                        active_session_id = self.load_session_id()
                    if active_session_id:
                        self._record_session_turn(active_session_id, session_mode)

                    return CommandResult(
                        success=True,
                        stdout=last_stdout,
                        stderr=last_stderr,
                        return_code=last_return_code,
                        duration_seconds=result.duration_seconds
                    )
                else:
                    logger.warning(
                        "OpenCode CLI 命令失败 (尝试 %s/%s, return_code=%s, duration=%.2fs)",
                        attempt + 1,
                        max_retries,
                        last_return_code,
                        result.duration_seconds,
                    )
                    if last_stderr:
                        logger.warning("错误输出(stderr):\n%s", self._truncate_for_log(last_stderr))
                    if last_stdout:
                        logger.warning("标准输出(stdout):\n%s", self._truncate_for_log(last_stdout))

                    if effective_use_resume and attempt == 0:
                        if runtime_error == "context_overflow":
                            logger.warning("检测到 OpenCode 上下文溢出，说明 auto compaction 未能恢复，清除 session 并降级为新会话执行")
                            self.save_session_id(None)
                        elif self._is_no_previous_session_error(last_stdout, last_stderr):
                            logger.warning("Resume 失败且会话不存在，清除 session 并降级执行")
                            self.save_session_id(None)
                        elif self._is_prompt_too_long_error(last_stdout or "", last_stderr or ""):
                            logger.warning("Prompt 超长（context overflow），清除 session 并降级执行")
                            self.save_session_id(None)
                        else:
                            logger.warning("Resume 失败但非会话缺失，保留 session 并降级执行")
                        effective_use_resume = False
                        cmd, should_save_session_id, session_mode = self._build_prompt_command(
                            base_cmd,
                            workdir,
                            prompt,
                            use_resume=False,
                        )
                    elif runtime_error == "context_overflow":
                        logger.error("OpenCode 新会话仍触发上下文溢出，停止重试以避免空转")
                        break

                    # Key rotation on API errors (env rebuilt per attempt)
                    if self._provider:
                        error_reason = self._classify_api_error(last_stdout, last_stderr)
                        if error_reason:
                            self._provider.report_failure(error_reason)

                    if attempt < max_retries - 1:
                        time.sleep(5)

            except Exception as e:
                logger.error(f"执行 OpenCode CLI 命令时出错: {e}")
                last_stderr = str(e)
                last_return_code = -1
                if attempt < max_retries - 1:
                    time.sleep(5)

        total_duration = time.time() - start_time
        logger.error(
            "OpenCode CLI 命令执行失败，已达到最大重试次数 (last_return_code=%s)",
            last_return_code,
        )
        return CommandResult(
            success=False,
            stdout=last_stdout,
            stderr=last_stderr,
            return_code=last_return_code,
            duration_seconds=total_duration
        )
