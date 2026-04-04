"""
System Under Test (SUT) Abstraction Module

This module provides a generic interface for defining and managing systems
that can be built, tested, and improved by AI code agents.

Example:
    >>> from sut import SystemUnderTest, register_sut, create_sut
    >>>
    >>> class MySystem(SystemUnderTest):
    ...     name = "my_system"
    ...     def start(self, config): ...
    ...     def stop(self): ...
    ...
    >>> register_sut("my_system", MySystem)
    >>> sut = create_sut("my_system", Path("./my_system_dir"))
"""

from .base import SystemUnderTest, SUTProcess
from .registry import (
    register_sut,
    unregister_sut,
    get_available_suts,
    get_sut_class,
    is_sut_registered,
    create_sut,
    list_suts_info,
)
from .config import SUTConfig, load_config

__all__ = [
    # Base classes
    "SystemUnderTest",
    "SUTProcess",
    # Registry functions
    "register_sut",
    "unregister_sut",
    "get_available_suts",
    "get_sut_class",
    "is_sut_registered",
    "create_sut",
    "list_suts_info",
    # Configuration
    "SUTConfig",
    "load_config",
]
