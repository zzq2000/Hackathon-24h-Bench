"""
Key rotation with cooldown management.

Supports multiple API keys per provider (semicolon-separated in env var)
with automatic rotation on failure and cooldown periods.
"""

import time
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class KeyState:
    """State tracking for a single API key."""

    key: str
    source: str  # env var name
    failure_count: int = 0
    last_failure_reason: str = ""
    cooldown_until: float = 0.0

    @property
    def is_in_cooldown(self) -> bool:
        return time.time() < self.cooldown_until

    @property
    def is_available(self) -> bool:
        return not self.is_in_cooldown


class KeyRotator:
    """
    Multi-key rotation with cooldown management.

    Keys are separated by semicolons in env vars:
        ANTHROPIC_API_KEY="sk-key1;sk-key2;sk-key3"

    Single-key usage is fully backward-compatible.
    """

    COOLDOWN_SECONDS: Dict[str, int] = {
        "rate_limit": 300,
        "auth": 3600,
        "billing": 86400,
        "unknown": 60,
    }

    def __init__(self, provider_name: str, keys: List[KeyState]):
        self.provider_name = provider_name
        self._keys = list(keys)
        self._current_index = 0

    @classmethod
    def from_env_value(cls, provider_name: str, env_value: str, source: str) -> "KeyRotator":
        """Create a KeyRotator from a (possibly semicolon-separated) env value."""
        raw_keys = [k.strip() for k in env_value.split(";") if k.strip()]
        if not raw_keys:
            return cls(provider_name, [])
        states = [KeyState(key=k, source=source) for k in raw_keys]
        return cls(provider_name, states)

    @property
    def key_count(self) -> int:
        return len(self._keys)

    @property
    def has_multiple_keys(self) -> bool:
        return len(self._keys) > 1

    def get_next_key(self) -> Optional[KeyState]:
        """Get the next available key, skipping those in cooldown."""
        if not self._keys:
            return None

        n = len(self._keys)
        for _ in range(n):
            ks = self._keys[self._current_index]
            self._current_index = (self._current_index + 1) % n
            if ks.is_available:
                return ks

        # All keys in cooldown; return the one with earliest cooldown expiry
        earliest = min(self._keys, key=lambda k: k.cooldown_until)
        logger.warning(
            "All %d keys for provider %s are in cooldown; returning least-recently-failed key (source=%s)",
            n,
            self.provider_name,
            earliest.source,
        )
        return earliest

    def report_failure(self, key: str, reason: str) -> None:
        """Report a key failure and apply cooldown."""
        cooldown = self.COOLDOWN_SECONDS.get(reason, self.COOLDOWN_SECONDS["unknown"])
        for ks in self._keys:
            if ks.key == key:
                ks.failure_count += 1
                ks.last_failure_reason = reason
                ks.cooldown_until = time.time() + cooldown
                logger.info(
                    "Key %s...%s marked failed (reason=%s, cooldown=%ds, total_failures=%d)",
                    key[:8],
                    key[-4:] if len(key) > 12 else "****",
                    reason,
                    cooldown,
                    ks.failure_count,
                )
                return

    def report_success(self, key: str) -> None:
        """Report a key success, resetting failure count."""
        for ks in self._keys:
            if ks.key == key:
                if ks.failure_count > 0:
                    logger.info(
                        "Key %s...%s recovered after %d failures",
                        key[:8],
                        key[-4:] if len(key) > 12 else "****",
                        ks.failure_count,
                    )
                ks.failure_count = 0
                ks.last_failure_reason = ""
                ks.cooldown_until = 0.0
                return
