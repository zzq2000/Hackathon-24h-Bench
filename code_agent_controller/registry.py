"""
代理注册表模块

提供代理类型的注册和工厂函数。
"""

import logging
from pathlib import Path
from typing import Dict, Type, Optional, Any, List

from .base import CodeAgentBase
from .agents import CodexAgent, ClaudeCodeAgent, GeminiCliAgent, KimiCodeAgent, OpenCodeAgent, QwenCodeAgent, GrokCliAgent, ClineAgent

logger = logging.getLogger(__name__)


# 代理注册表 - 存储所有已注册的代理类型
_AGENT_REGISTRY: Dict[str, Type[CodeAgentBase]] = {}


def _register_builtin_agents() -> None:
    """注册内置代理"""
    _AGENT_REGISTRY["codex"] = CodexAgent
    _AGENT_REGISTRY["claude"] = ClaudeCodeAgent
    _AGENT_REGISTRY["gemini"] = GeminiCliAgent
    _AGENT_REGISTRY["kimi"] = KimiCodeAgent
    _AGENT_REGISTRY["opencode"] = OpenCodeAgent
    _AGENT_REGISTRY["qwen"] = QwenCodeAgent
    _AGENT_REGISTRY["grok"] = GrokCliAgent
    _AGENT_REGISTRY["cline"] = ClineAgent


# 初始化时注册内置代理
_register_builtin_agents()


def register_agent(name: str, agent_class: Type[CodeAgentBase]) -> None:
    """
    注册新的代理类型

    通过此函数可以扩展支持自定义的代码代理。

    Args:
        name: 代理名称（用于命令行选择）
        agent_class: 代理类（必须继承自 CodeAgentBase）

    Raises:
        ValueError: 如果 agent_class 不是 CodeAgentBase 的子类

    Example:
        >>> from code_agent_controller import CodeAgentBase, register_agent
        >>>
        >>> class MyCustomAgent(CodeAgentBase):
        ...     name = "custom"
        ...
        ...     def check_cli(self) -> bool:
        ...         return True
        ...
        ...     def check_api_key(self) -> bool:
        ...         return True
        ...
        ...     def run_command(self, prompt, use_resume=False, max_retries=3) -> CommandResult:
        ...         print(f"Running: {prompt}")
        ...         return True
        >>>
        >>> register_agent("custom", MyCustomAgent)
    """
    if not issubclass(agent_class, CodeAgentBase):
        raise ValueError(f"agent_class 必须继承自 CodeAgentBase，但收到: {agent_class}")

    if name in _AGENT_REGISTRY:
        logger.warning(f"覆盖已存在的代理: {name}")

    _AGENT_REGISTRY[name] = agent_class
    logger.info(f"已注册代理: {name}")


def unregister_agent(name: str) -> bool:
    """
    注销代理类型

    Args:
        name: 代理名称

    Returns:
        是否成功注销
    """
    if name in _AGENT_REGISTRY:
        del _AGENT_REGISTRY[name]
        logger.info(f"已注销代理: {name}")
        return True
    return False


def get_available_agents() -> List[str]:
    """
    获取所有可用的代理名称列表

    Returns:
        代理名称列表
    """
    return list(_AGENT_REGISTRY.keys())


def get_agent_class(name: str) -> Optional[Type[CodeAgentBase]]:
    """
    获取代理类

    Args:
        name: 代理名称

    Returns:
        代理类或 None
    """
    return _AGENT_REGISTRY.get(name.lower())


def is_agent_registered(name: str) -> bool:
    """
    检查代理是否已注册

    Args:
        name: 代理名称

    Returns:
        是否已注册
    """
    return name.lower() in _AGENT_REGISTRY


def create_agent(
    agent_name: str,
    sut_dir: Path,
    config: Optional[Dict[str, Any]] = None
) -> CodeAgentBase:
    """
    创建代理实例的工厂函数

    Args:
        agent_name: 代理名称 (codex, claude, gemini, kimi, 或自定义名称)
        sut_dir: SUT（System Under Test）工作目录
        config: 可选的配置字典

    Returns:
        代理实例

    Raises:
        ValueError: 如果代理名称未注册

    Example:
        >>> from code_agent_controller import create_agent
        >>> from pathlib import Path
        >>>
        >>> agent = create_agent("codex", Path("./my_sut"))
        >>> agent.initialize_database()
    """
    agent_name = agent_name.lower()
    if agent_name not in _AGENT_REGISTRY:
        available = ", ".join(_AGENT_REGISTRY.keys())
        raise ValueError(f"未知的代理类型: {agent_name}。可用的代理: {available}")

    agent_class = _AGENT_REGISTRY[agent_name]
    return agent_class(sut_dir, config)


def list_agents_info() -> Dict[str, Dict[str, Any]]:
    """
    获取所有代理的详细信息

    Returns:
        代理信息字典，键为代理名称，值为包含描述等信息的字典
    """
    info = {}
    for name, agent_class in _AGENT_REGISTRY.items():
        info[name] = {
            "class": agent_class.__name__,
            "module": agent_class.__module__,
            "doc": agent_class.__doc__.strip().split('\n')[0] if agent_class.__doc__ else "",
        }
    return info
