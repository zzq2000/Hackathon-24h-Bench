"""
Core data structures and registry for unified provider management.

Loads providers.yaml + providers.local.yaml and provides resolution methods
for agents to obtain API keys, base URLs, and model configuration.
"""

import os
import re
import copy
import logging
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    FrozenSet,
    List,
    Optional,
    Sequence,
    Tuple,
)

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

from .rotation import KeyRotator

logger = logging.getLogger(__name__)

_WORK_DIR = Path(__file__).resolve().parent.parent.parent
_DEFAULT_CONFIG_PATH = _WORK_DIR / "config" / "providers.yaml"
_LOCAL_CONFIG_PATH = _WORK_DIR / "config" / "providers.local.yaml"
_BAILIAN_MODEL_PREFIX = "bailian-coding-plan/"


class ProviderType(str, Enum):
    """Provider type classification."""

    NATIVE = "native"
    GATEWAY = "gateway"
    PROXY = "proxy"


@dataclass(frozen=True)
class ProviderDef:
    """Immutable provider definition loaded from providers.yaml."""

    name: str
    display_name: str
    provider_type: ProviderType
    api_type: str  # "anthropic" / "openai" / "google"
    api_key_env: Tuple[str, ...]
    api_key_mirror: Dict[str, str] = field(default_factory=dict)
    base_url_env: Optional[str] = None
    default_base_url: Optional[str] = None
    fallback_base_urls: Tuple[str, ...] = ()
    extra_env: Dict[str, str] = field(default_factory=dict)
    extra_headers: Dict[str, str] = field(default_factory=dict)
    parent_provider: Optional[str] = None
    auth_alternatives: Tuple[str, ...] = ()
    model_prefix: str = ""
    allow_any_model: bool = False
    default_model: Optional[str] = None

    @property
    def is_proxy(self) -> bool:
        return self.provider_type == ProviderType.PROXY

    @property
    def is_gateway(self) -> bool:
        return self.provider_type == ProviderType.GATEWAY


@dataclass(frozen=True)
class ModelDef:
    """Model catalog entry."""

    name: str
    provider: str
    aliases: Tuple[str, ...] = ()
    tags: FrozenSet[str] = frozenset()


@dataclass
class ResolvedProvider:
    """Fully resolved provider configuration for an agent invocation."""

    provider_name: str
    provider_type: ProviderType
    api_type: str
    api_key: str
    api_key_source: str
    base_url: Optional[str] = None
    base_url_env_key: Optional[str] = None  # Which env var to set for base URL
    model: Optional[str] = None
    display_model: Optional[str] = None
    extra_env: Dict[str, str] = field(default_factory=dict)
    extra_headers: Dict[str, str] = field(default_factory=dict)
    env_mirrors: Dict[str, str] = field(default_factory=dict)
    _rotator: Optional[KeyRotator] = field(default=None, repr=False, compare=False)

    @property
    def has_key_rotation(self) -> bool:
        """Whether this provider has multiple keys for rotation."""
        return self._rotator is not None and self._rotator.has_multiple_keys

    def report_success(self) -> None:
        """Report that the current API key worked successfully."""
        if self._rotator:
            self._rotator.report_success(self.api_key)

    def report_failure(self, reason: str = "unknown") -> bool:
        """Report API key failure and rotate to the next available key.

        Returns True if the key was actually changed (rotation occurred).
        """
        if not self._rotator:
            return False
        self._rotator.report_failure(self.api_key, reason)
        next_ks = self._rotator.get_next_key()
        if next_ks and next_ks.key != self.api_key:
            old_key_hint = f"{self.api_key[:8]}...{self.api_key[-4:]}" if len(self.api_key) > 12 else "****"
            new_key_hint = f"{next_ks.key[:8]}...{next_ks.key[-4:]}" if len(next_ks.key) > 12 else "****"
            logger.info(
                "Key rotated for provider %s: %s -> %s (reason=%s)",
                self.provider_name, old_key_hint, new_key_hint, reason,
            )
            self.api_key = next_ks.key
            self.api_key_source = next_ks.source
            return True
        return False

    def build_env_dict(self) -> Dict[str, str]:
        """Build a complete env dict suitable for subprocess calls."""
        env = {**os.environ}

        # Set the API key in the source env var
        env[self.api_key_source] = self.api_key

        # Apply mirrors
        for src, dst in self.env_mirrors.items():
            if src in env and not env.get(dst):
                env[dst] = env[src]

        # Apply base URL using the provider's own env var key
        if self.base_url and self.base_url_env_key:
            env.setdefault(self.base_url_env_key, self.base_url)

        # Apply extra env (with ${VAR:-default} interpolation)
        for key, raw_value in self.extra_env.items():
            env.setdefault(key, _interpolate_env_value(raw_value, env))

        return env

    @property
    def is_proxy(self) -> bool:
        return self.provider_type == ProviderType.PROXY


def _interpolate_env_value(raw: str, env: Dict[str, str]) -> str:
    """Expand ${VAR:-default} patterns in a string."""

    def _replacer(m: re.Match) -> str:
        var_name = m.group(1)
        default = m.group(2) if m.group(2) is not None else ""
        return env.get(var_name, default)

    return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}", _replacer, raw)


def _deep_merge(base: dict, overlay: dict) -> dict:
    """Deep merge overlay into base (non-destructive to base)."""
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def _to_tuple_of_str(value: Any) -> Tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(v) for v in value)
    return (str(value),)


def _to_dict_str(value: Any) -> Dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(k): str(v) for k, v in value.items()}


def _parse_provider_def(name: str, raw: Dict[str, Any]) -> ProviderDef:
    """Parse a raw YAML dict into a ProviderDef."""
    ptype_str = str(raw.get("type", "native")).lower()
    try:
        ptype = ProviderType(ptype_str)
    except ValueError:
        logger.warning("Unknown provider type %r for %s, defaulting to native", ptype_str, name)
        ptype = ProviderType.NATIVE

    return ProviderDef(
        name=name,
        display_name=str(raw.get("display_name", name)),
        provider_type=ptype,
        api_type=str(raw.get("api_type", "openai")),
        api_key_env=_to_tuple_of_str(raw.get("api_key_env")),
        api_key_mirror=_to_dict_str(raw.get("api_key_mirror")),
        base_url_env=raw.get("base_url_env"),
        default_base_url=raw.get("default_base_url"),
        fallback_base_urls=_to_tuple_of_str(raw.get("fallback_base_urls")),
        extra_env=_to_dict_str(raw.get("extra_env")),
        extra_headers=_to_dict_str(raw.get("extra_headers")),
        parent_provider=raw.get("parent_provider"),
        auth_alternatives=_to_tuple_of_str(raw.get("auth_alternatives")),
        model_prefix=str(raw.get("model_prefix", "")),
        allow_any_model=bool(raw.get("allow_any_model", False)),
        default_model=raw.get("default_model"),
    )


def _parse_model_def(name: str, raw: Dict[str, Any]) -> ModelDef:
    """Parse a raw YAML dict into a ModelDef."""
    aliases = _to_tuple_of_str(raw.get("aliases"))
    tags_raw = raw.get("tags")
    if isinstance(tags_raw, (list, tuple)):
        tags = frozenset(str(t) for t in tags_raw)
    elif isinstance(tags_raw, str):
        tags = frozenset([tags_raw])
    else:
        tags = frozenset()
    return ModelDef(
        name=name,
        provider=str(raw.get("provider", "")),
        aliases=aliases,
        tags=tags,
    )


class ProviderRegistry:
    """
    Singleton registry that loads providers.yaml + providers.local.yaml
    and provides resolution methods.
    """

    _instance: Optional["ProviderRegistry"] = None

    @classmethod
    def get_instance(cls) -> "ProviderRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton (mainly for testing)."""
        cls._instance = None

    def __init__(
        self,
        config_path: Optional[Path] = None,
        local_config_path: Optional[Path] = None,
    ):
        self._providers: Dict[str, ProviderDef] = {}
        self._models: Dict[str, ModelDef] = {}
        # Lowercase alias -> canonical model name
        self._model_alias_map: Dict[str, str] = {}
        self._agent_providers: Dict[str, Dict[str, Any]] = {}
        # KeyRotator instances keyed by "provider_name:env_var_name"
        self._rotators: Dict[str, KeyRotator] = {}

        self._load(
            config_path or _DEFAULT_CONFIG_PATH,
            local_config_path or _LOCAL_CONFIG_PATH,
        )

    def _load(self, base_path: Path, local_path: Path) -> None:
        if yaml is None:
            logger.warning("PyYAML not installed; provider registry will be empty")
            return

        raw: Dict[str, Any] = {}
        if base_path.exists():
            try:
                raw = yaml.safe_load(base_path.read_text(encoding="utf-8")) or {}
            except Exception as exc:
                logger.warning("Failed to load %s: %s", base_path, exc)

        if local_path.exists():
            try:
                local_raw = yaml.safe_load(local_path.read_text(encoding="utf-8")) or {}
                raw = _deep_merge(raw, local_raw)
            except Exception as exc:
                logger.warning("Failed to load %s: %s", local_path, exc)

        # Parse providers
        for name, pdef_raw in (raw.get("providers") or {}).items():
            if not isinstance(pdef_raw, dict):
                continue
            self._providers[name] = _parse_provider_def(name, pdef_raw)

        # Parse model catalog
        for name, mdef_raw in (raw.get("model_catalog") or {}).items():
            if not isinstance(mdef_raw, dict):
                continue
            mdef = _parse_model_def(name, mdef_raw)
            self._models[name] = mdef
            # Build alias map (case-insensitive)
            self._model_alias_map[name.lower()] = name
            for alias in mdef.aliases:
                self._model_alias_map[alias.lower()] = name

        # Parse agent_providers
        for agent_name, agent_raw in (raw.get("agent_providers") or {}).items():
            if not isinstance(agent_raw, dict):
                continue
            self._agent_providers[agent_name] = agent_raw

    # ------------------------------------------------------------------
    # Public query methods
    # ------------------------------------------------------------------

    def get_provider_def(self, provider_name: str) -> Optional[ProviderDef]:
        return self._providers.get(provider_name)

    def get_model_def(self, model_name: str) -> Optional[ModelDef]:
        """Look up a model by canonical name or alias (case-insensitive)."""
        canonical = self._model_alias_map.get(model_name.lower())
        if canonical:
            return self._models.get(canonical)
        return self._models.get(model_name)

    def normalize_model(self, model_name: str) -> str:
        """Strip bailian-coding-plan/ prefix and return the bare canonical name."""
        if not model_name:
            return model_name
        stripped = model_name.strip()
        lower = stripped.lower()
        if lower.startswith(_BAILIAN_MODEL_PREFIX):
            stripped = stripped[len(_BAILIAN_MODEL_PREFIX):]
        # Check alias map for canonical casing
        canonical = self._model_alias_map.get(stripped.lower())
        if canonical:
            return canonical
        return stripped

    def strip_model_prefix(self, model_name: str) -> str:
        """Strip bailian-coding-plan/ prefix, preserving original casing."""
        if not model_name:
            return model_name
        stripped = model_name.strip()
        if stripped.lower().startswith(_BAILIAN_MODEL_PREFIX):
            return stripped[len(_BAILIAN_MODEL_PREFIX):]
        return stripped

    def is_bailian_model(self, model_name: str) -> bool:
        return self.has_tag(model_name, "bailian")

    def has_tag(self, model_name: str, tag: str) -> bool:
        """Check if a model has a specific tag in the catalog."""
        if not model_name:
            return False
        normalized = self.normalize_model(model_name)
        mdef = self.get_model_def(normalized)
        if mdef and tag in mdef.tags:
            return True
        return False

    def list_providers(self, provider_type: Optional[ProviderType] = None) -> List[ProviderDef]:
        """List all providers, optionally filtered by type."""
        if provider_type is None:
            return list(self._providers.values())
        return [p for p in self._providers.values() if p.provider_type == provider_type]

    def get_all_env_keys_for_agent(self, agent_name: str) -> List[str]:
        """Return all env var keys that an agent might need (for Docker passthrough)."""
        agent_cfg = self._agent_providers.get(agent_name, {})
        provider_names = agent_cfg.get("providers", [])
        extra_providers = agent_cfg.get("extra_providers", [])
        all_provider_names = list(provider_names) + list(extra_providers)

        keys: List[str] = []
        seen: set = set()

        def _add(k: str) -> None:
            if k and k not in seen:
                seen.add(k)
                keys.append(k)

        # Model env
        model_env = agent_cfg.get("model_env")
        if model_env:
            _add(model_env)
        _add("CODE_AGENT_MODEL")

        # Provider env
        provider_env = agent_cfg.get("provider_env")
        if provider_env:
            _add(provider_env)

        # Collect keys from all providers
        for pname in all_provider_names:
            pdef = self._providers.get(pname)
            if not pdef:
                continue
            for k in pdef.api_key_env:
                _add(k)
            if pdef.base_url_env:
                _add(pdef.base_url_env)
            for k in pdef.api_key_mirror.values():
                _add(k)
            for k in pdef.auth_alternatives:
                _add(k)
            for k in pdef.extra_env:
                _add(k)

        # Common control env vars
        for k in (
            "CODE_AGENT_WAIT_TIME",
            "CODE_AGENT_MAX_RETRIES",
            "CODE_AGENT_COMMAND_TIMEOUT",
            "AGENT_WAIT_TIME",
            "AGENT_MAX_RETRIES",
            "AGENT_COMMAND_TIMEOUT",
            "CODE_AGENT_LOG_OUTPUT_MAX_CHARS",
        ):
            _add(k)

        return keys

    def register_provider(self, provider_def: ProviderDef) -> None:
        """Register a provider at runtime (for plugins / custom agents)."""
        self._providers[provider_def.name] = provider_def

    # ------------------------------------------------------------------
    # Resolution methods
    # ------------------------------------------------------------------

    def resolve_provider(
        self,
        agent_name: str,
        *,
        model: Optional[str] = None,
        provider_hint: Optional[str] = None,
    ) -> Optional[ResolvedProvider]:
        """
        Resolve a provider for the given agent.

        Priority:
        1. explicit provider_hint (from config/env/CLI)
        2. model catalog auto-detect (native/gateway)
        3. first native/gateway provider with valid key from agent_providers list
        """
        agent_cfg = self._agent_providers.get(agent_name, {})
        provider_names: List[str] = list(agent_cfg.get("providers", []))
        extra_providers: List[str] = list(agent_cfg.get("extra_providers", []))
        provider_names.extend(extra_providers)
        provider_aliases: Dict[str, str] = agent_cfg.get("provider_aliases", {})

        # 1. Explicit provider hint
        if provider_hint:
            resolved_name = provider_aliases.get(provider_hint.lower(), provider_hint)
            pdef = self._providers.get(resolved_name)
            if pdef:
                if pdef.is_proxy:
                    return self.resolve_proxy(resolved_name, model=model)
                return self._try_resolve(pdef, model=model)

        # 2. Model catalog auto-detect
        if model:
            normalized = self.normalize_model(model)
            mdef = self.get_model_def(normalized)
            if mdef and mdef.provider:
                pdef = self._providers.get(mdef.provider)
                if pdef and pdef.name in provider_names:
                    resolved = self._try_resolve(pdef, model=normalized)
                    if resolved:
                        return resolved

        # 3. Walk agent provider list
        for pname in provider_names:
            pdef = self._providers.get(pname)
            if not pdef:
                continue
            if pdef.is_proxy:
                continue  # skip proxy in auto-walk
            resolved = self._try_resolve(pdef, model=model)
            if resolved:
                return resolved

        return None

    def resolve_proxy(
        self,
        provider_name: str,
        *,
        model: Optional[str] = None,
    ) -> Optional[ResolvedProvider]:
        """Resolve a proxy provider (LiteLLM/OpenRouter/Azure/custom)."""
        pdef = self._providers.get(provider_name)
        if not pdef:
            return None

        api_key, key_source, rotator = self._find_api_key(pdef)
        if not api_key:
            return None

        base_url = self._find_base_url(pdef)
        if not base_url:
            return None

        env_for_interpolation = {**os.environ}
        extra_env = {k: _interpolate_env_value(v, env_for_interpolation) for k, v in pdef.extra_env.items()}
        extra_headers = {k: _interpolate_env_value(v, env_for_interpolation) for k, v in pdef.extra_headers.items()}

        # For proxy, model is passed through as-is
        effective_model = model
        if not effective_model and pdef.default_model:
            effective_model = pdef.default_model

        return ResolvedProvider(
            provider_name=pdef.name,
            provider_type=pdef.provider_type,
            api_type=pdef.api_type,
            api_key=api_key,
            api_key_source=key_source,
            base_url=base_url,
            base_url_env_key=pdef.base_url_env,
            model=effective_model,
            display_model=effective_model,
            extra_env=extra_env,
            extra_headers=extra_headers,
            env_mirrors={},
            _rotator=rotator,
        )

    def _try_resolve(
        self,
        pdef: ProviderDef,
        *,
        model: Optional[str] = None,
    ) -> Optional[ResolvedProvider]:
        """Try to resolve a native/gateway provider."""
        api_key, key_source, rotator = self._find_api_key(pdef)

        # For providers with auth_alternatives, check those too
        if not api_key and pdef.auth_alternatives:
            for alt_key in pdef.auth_alternatives:
                alt_val = (os.environ.get(alt_key) or "").strip()
                if alt_val:
                    # Use a sentinel to indicate non-key auth
                    api_key = f"__auth_alternative__{alt_key}"
                    key_source = alt_key
                    break

        if not api_key:
            return None

        base_url = self._find_base_url(pdef)

        # Build env mirrors
        env_mirrors: Dict[str, str] = {}
        for src, dst in pdef.api_key_mirror.items():
            env_mirrors[src] = dst

        # Strip prefix for gateway but preserve original casing
        effective_model = model
        if model and pdef.is_gateway:
            effective_model = self.strip_model_prefix(model)

        env_for_interpolation = {**os.environ}
        extra_env = {k: _interpolate_env_value(v, env_for_interpolation) for k, v in pdef.extra_env.items()}

        return ResolvedProvider(
            provider_name=pdef.name,
            provider_type=pdef.provider_type,
            api_type=pdef.api_type,
            api_key=api_key,
            api_key_source=key_source,
            base_url=base_url,
            base_url_env_key=pdef.base_url_env,
            model=effective_model,
            display_model=model,
            extra_env=extra_env,
            extra_headers={},
            env_mirrors=env_mirrors,
            _rotator=rotator,
        )

    def _find_api_key(self, pdef: ProviderDef) -> Tuple[Optional[str], str, Optional[KeyRotator]]:
        """Find the first available API key from the provider's env var list.

        When an env var contains semicolon-separated keys (e.g. ``sk-1;sk-2``),
        a :class:`KeyRotator` is created (or reused) and the next available key
        is returned.  Single-key usage is fully backward-compatible.

        Returns:
            (api_key, env_var_name, rotator_or_None)
        """
        for key_name in pdef.api_key_env:
            value = (os.environ.get(key_name) or "").strip()
            if value:
                if ";" in value:
                    rotator_id = f"{pdef.name}:{key_name}"
                    if rotator_id not in self._rotators:
                        self._rotators[rotator_id] = KeyRotator.from_env_value(
                            pdef.name, value, key_name,
                        )
                        logger.info(
                            "Created KeyRotator for provider %s (env=%s, keys=%d)",
                            pdef.name, key_name, self._rotators[rotator_id].key_count,
                        )
                    rotator = self._rotators[rotator_id]
                    ks = rotator.get_next_key()
                    if ks:
                        return ks.key, ks.source, rotator
                return value, key_name, None
        return None, "", None

    def _find_base_url(self, pdef: ProviderDef) -> Optional[str]:
        """Resolve the base URL for a provider.

        Explicit env var (e.g. ``ANTHROPIC_BASE_URL``) always takes priority
        so users can override the gateway's default URL at the command line.
        Falls back to ``default_base_url`` from the provider definition.
        """
        if pdef.base_url_env:
            explicit = (os.environ.get(pdef.base_url_env) or "").strip()
            if explicit:
                return explicit
        return pdef.default_base_url
