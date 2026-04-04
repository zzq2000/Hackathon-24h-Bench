"""
Unified Provider / API Key / Model management.

Public API:
    ProviderRegistry  – singleton registry (loads providers.yaml)
    ProviderType      – native / gateway / proxy enum
    ProviderDef       – immutable provider definition
    ModelDef          – model catalog entry
    ResolvedProvider  – fully resolved provider for a specific agent call
    KeyRotator        – multi-key rotation with cooldown
"""

from .config import (
    ProviderType,
    ProviderDef,
    ModelDef,
    ResolvedProvider,
    ProviderRegistry,
)
from .rotation import KeyState, KeyRotator

__all__ = [
    "ProviderType",
    "ProviderDef",
    "ModelDef",
    "ResolvedProvider",
    "ProviderRegistry",
    "KeyState",
    "KeyRotator",
]
