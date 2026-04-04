"""
SUT Registry Module

Provides registration and factory functions for System Under Test types.
"""

import logging
from pathlib import Path
from typing import Dict, Type, Optional, Any, List

from .base import SystemUnderTest

logger = logging.getLogger(__name__)


# SUT registry - stores all registered SUT types
_SUT_REGISTRY: Dict[str, Type[SystemUnderTest]] = {}


def _register_builtin_suts() -> None:
    """Register built-in SUT implementations."""
    # Import will be done after implementations are created
    try:
        from .implementations.database import DatabaseSUT
        _SUT_REGISTRY["database"] = DatabaseSUT
    except ImportError:
        logger.debug("Database SUT implementation not available")

    try:
        from .implementations.message_queue import MessageQueueSUT
        _SUT_REGISTRY["message_queue"] = MessageQueueSUT
    except ImportError:
        logger.debug("Message Queue SUT implementation not available")

    try:
        from .implementations.http_server import HttpServerSUT
        _SUT_REGISTRY["http_server"] = HttpServerSUT
    except ImportError:
        logger.debug("HTTP Server SUT implementation not available")

    try:
        from .implementations.redis_kvstore import RedisKVStoreSUT
        _SUT_REGISTRY["redis_kvstore"] = RedisKVStoreSUT
    except ImportError:
        logger.debug("Redis KV Store SUT implementation not available")


def register_sut(name: str, sut_class: Type[SystemUnderTest]) -> None:
    """
    Register a new SUT type.

    This function allows extending the framework with custom system types.

    Args:
        name: SUT name (used for CLI selection and config)
        sut_class: SUT class (must inherit from SystemUnderTest)

    Raises:
        ValueError: If sut_class is not a SystemUnderTest subclass

    Example:
        >>> from sut import SystemUnderTest, register_sut
        >>>
        >>> class MyCustomSUT(SystemUnderTest):
        ...     name = "custom"
        ...
        ...     def start(self, host, port): ...
        ...     def check_ready(self, host, port, timeout): ...
        ...     def stop(self): ...
        ...     def get_init_prompt(self): ...
        ...     def get_improve_prompt(self, iteration, feedback): ...
        >>>
        >>> register_sut("custom", MyCustomSUT)
    """
    if not issubclass(sut_class, SystemUnderTest):
        raise ValueError(
            f"sut_class must inherit from SystemUnderTest, got: {sut_class}"
        )

    if name in _SUT_REGISTRY:
        logger.warning(f"Overriding existing SUT type: {name}")

    _SUT_REGISTRY[name] = sut_class
    logger.info(f"Registered SUT type: {name}")


def unregister_sut(name: str) -> bool:
    """
    Unregister a SUT type.

    Args:
        name: SUT name

    Returns:
        True if successfully unregistered
    """
    if name in _SUT_REGISTRY:
        del _SUT_REGISTRY[name]
        logger.info(f"Unregistered SUT type: {name}")
        return True
    return False


def get_available_suts() -> List[str]:
    """
    Get all available SUT type names.

    Returns:
        List of SUT names
    """
    return list(_SUT_REGISTRY.keys())


def get_sut_class(name: str) -> Optional[Type[SystemUnderTest]]:
    """
    Get a SUT class by name.

    Args:
        name: SUT name

    Returns:
        SUT class or None
    """
    return _SUT_REGISTRY.get(name.lower())


def is_sut_registered(name: str) -> bool:
    """
    Check if a SUT type is registered.

    Args:
        name: SUT name

    Returns:
        True if registered
    """
    return name.lower() in _SUT_REGISTRY


def create_sut(
    sut_name: str,
    work_dir: Path,
    config: Optional[Dict[str, Any]] = None
) -> SystemUnderTest:
    """
    Create a SUT instance.

    Factory function for creating SUT instances.

    Args:
        sut_name: SUT type name (database, message_queue, etc.)
        work_dir: Working directory for the system
        config: Optional configuration dictionary

    Returns:
        SUT instance

    Raises:
        ValueError: If SUT name is not registered

    Example:
        >>> from sut import create_sut
        >>> from pathlib import Path
        >>>
        >>> sut = create_sut("database", Path("./my_database"))
        >>> sut.start(host="127.0.0.1", port=3307)
    """
    sut_name = sut_name.lower()
    if sut_name not in _SUT_REGISTRY:
        available = ", ".join(_SUT_REGISTRY.keys())
        raise ValueError(
            f"Unknown SUT type: {sut_name}. Available types: {available}"
        )

    sut_class = _SUT_REGISTRY[sut_name]
    return sut_class(work_dir, config)


def list_suts_info() -> Dict[str, Dict[str, Any]]:
    """
    Get detailed information about all registered SUTs.

    Returns:
        Dictionary with SUT info, keyed by name
    """
    info = {}
    for name, sut_class in _SUT_REGISTRY.items():
        info[name] = {
            "class": sut_class.__name__,
            "module": sut_class.__module__,
            "description": getattr(sut_class, "description", ""),
            "default_port": getattr(sut_class, "default_port", 0),
            "doc": (
                sut_class.__doc__.strip().split('\n')[0]
                if sut_class.__doc__
                else ""
            ),
        }
    return info


# Initialize registry with built-in SUTs
# Note: This is called at module import time, but implementations
# may not be available yet. Call again after implementations are loaded.
_register_builtin_suts()
