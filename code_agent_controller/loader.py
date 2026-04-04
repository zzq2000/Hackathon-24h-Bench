"""
Custom agent loader module.

Provides functionality to dynamically load custom agent implementations
from a directory at runtime.
"""

import os
import sys
import logging
import importlib.util
from pathlib import Path
from typing import List, Optional

from .registry import register_agent, is_agent_registered
from .base import CodeAgentBase

logger = logging.getLogger(__name__)


def load_custom_agents(custom_dir: Optional[Path] = None) -> List[str]:
    """
    Load custom agent implementations from a directory.

    Scans the specified directory for Python files and attempts to load them.
    Files should contain classes that inherit from CodeAgentBase and call
    register_agent() to register themselves.

    Args:
        custom_dir: Path to directory containing custom agent files.
                   If None, uses CUSTOM_AGENTS_DIR environment variable.

    Returns:
        List of successfully loaded agent names.

    Example:
        Custom agent file (my_agent.py):

        ```python
        from code_agent_controller import CodeAgentBase, register_agent

        class MyCustomAgent(CodeAgentBase):
            name = "my-agent"

            def check_cli(self) -> bool:
                return True

            def check_api_key(self) -> bool:
                return True

            def run_command(self, prompt, use_resume=False, max_retries=3) -> bool:
                # Implementation
                return True

        register_agent("my-agent", MyCustomAgent)
        ```
    """
    if custom_dir is None:
        env_dir = os.environ.get("CUSTOM_AGENTS_DIR")
        if not env_dir:
            logger.debug("No custom agents directory specified")
            return []
        custom_dir = Path(env_dir)

    custom_dir = Path(custom_dir)
    if not custom_dir.exists():
        logger.debug(f"Custom agents directory does not exist: {custom_dir}")
        return []

    if not custom_dir.is_dir():
        logger.warning(f"Custom agents path is not a directory: {custom_dir}")
        return []

    loaded_agents = []

    # Find all Python files
    py_files = list(custom_dir.glob("*.py"))
    if not py_files:
        logger.debug(f"No Python files found in {custom_dir}")
        return []

    logger.info(f"Loading custom agents from {custom_dir}")

    for py_file in py_files:
        if py_file.name.startswith("_"):
            # Skip private files
            continue

        try:
            agent_names = _load_agent_file(py_file)
            loaded_agents.extend(agent_names)
        except Exception as e:
            logger.error(f"Failed to load custom agent from {py_file}: {e}")

    if loaded_agents:
        logger.info(f"Loaded custom agents: {', '.join(loaded_agents)}")

    return loaded_agents


def _load_agent_file(py_file: Path) -> List[str]:
    """
    Load a single agent file and return registered agent names.

    Args:
        py_file: Path to Python file

    Returns:
        List of agent names registered by this file
    """
    module_name = f"custom_agent_{py_file.stem}"

    # Get currently registered agents before loading
    from .registry import get_available_agents
    agents_before = set(get_available_agents())

    # Load the module
    spec = importlib.util.spec_from_file_location(module_name, py_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec from {py_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        # Clean up on failure
        if module_name in sys.modules:
            del sys.modules[module_name]
        raise ImportError(f"Error executing module {py_file}: {e}") from e

    # Find newly registered agents
    agents_after = set(get_available_agents())
    new_agents = list(agents_after - agents_before)

    if new_agents:
        logger.debug(f"Loaded agents from {py_file.name}: {', '.join(new_agents)}")
    else:
        logger.warning(f"No agents registered from {py_file.name}")

    return new_agents


def discover_agent_classes(module) -> List[type]:
    """
    Discover CodeAgentBase subclasses in a module.

    Args:
        module: Loaded Python module

    Returns:
        List of agent classes found in the module
    """
    agent_classes = []

    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, CodeAgentBase)
            and obj is not CodeAgentBase
            and hasattr(obj, "name")
        ):
            agent_classes.append(obj)

    return agent_classes


def validate_agent_class(agent_class: type) -> bool:
    """
    Validate that an agent class implements required methods.

    Args:
        agent_class: Agent class to validate

    Returns:
        True if valid
    """
    required_methods = ["check_cli", "check_api_key", "run_command"]

    for method in required_methods:
        if not hasattr(agent_class, method):
            logger.error(f"Agent class {agent_class.__name__} missing method: {method}")
            return False

        # Check it's actually callable
        attr = getattr(agent_class, method)
        if not callable(attr):
            logger.error(f"Agent class {agent_class.__name__}.{method} is not callable")
            return False

    # Check name attribute
    if not hasattr(agent_class, "name") or not agent_class.name:
        logger.error(f"Agent class {agent_class.__name__} missing 'name' attribute")
        return False

    return True
