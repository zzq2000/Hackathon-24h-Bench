"""
Code Agent Controller - 可扩展的代码代理控制器

支持多种代码代理工具：
- Codex CLI (OpenAI)
- Claude Code (Anthropic)
- Gemini CLI (Google)
- Kimi Code CLI (Moonshot)

可以通过继承 CodeAgentBase 类来扩展支持其他代码代理工具。

基本用法:
    # 命令行使用
    python -m code_agent_controller --agent codex --sut-dir ./database

    # 编程方式使用
    from code_agent_controller import create_agent
    agent = create_agent("codex", Path("./database"))
    agent.initialize_database()

扩展自定义代理:
    from code_agent_controller import CodeAgentBase, register_agent

    class MyCustomAgent(CodeAgentBase):
        name = "custom"

        def check_cli(self) -> bool:
            # 检查 CLI 工具
            return True

        def check_api_key(self) -> bool:
            # 检查 API 密钥
            return True

        def run_command(self, prompt, use_resume=False, max_retries=3) -> CommandResult:
            # 执行命令
            return CommandResult(success=True)

    register_agent("custom", MyCustomAgent)
"""

__version__ = "1.0.0"
__author__ = "Hackathon-24h-Bench Team"

# 核心类
from .base import CodeAgentBase

# 内置代理实现
from .agents import CodexAgent, ClaudeCodeAgent, GeminiCliAgent, KimiCodeAgent, ClineAgent

# 注册表和工厂函数
from .registry import (
    register_agent,
    unregister_agent,
    get_available_agents,
    get_agent_class,
    is_agent_registered,
    create_agent,
    list_agents_info,
)

# 控制器
from .controller import run_controller, run_docker_controller, main

# Docker runner
from .docker_runner import (
    DockerAgentRunner,
    check_docker_available,
    DEFAULT_IMAGE_NAME,
    CONTAINER_SUT_DIR,
    CONTAINER_SESSION_DIR,
)

# Custom agent loader
from .loader import load_custom_agents, validate_agent_class

# Container mode utilities
from .base import is_container_mode, get_session_dir, get_container_workdir

# 工具函数
from .utils import (
    WORK_DIR,
    load_env_file,
    setup_logging,
    ensure_directory,
    has_sut_files,
    get_env,
    get_env_bool,
    CommandResult,
    LogManager,
)

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    # 核心类
    "CodeAgentBase",
    # 内置代理
    "CodexAgent",
    "ClaudeCodeAgent",
    "GeminiCliAgent",
    "KimiCodeAgent",
    "ClineAgent",
    # 注册表函数
    "register_agent",
    "unregister_agent",
    "get_available_agents",
    "get_agent_class",
    "is_agent_registered",
    "create_agent",
    "list_agents_info",
    # 控制器
    "run_controller",
    "run_docker_controller",
    "main",
    # Docker runner
    "DockerAgentRunner",
    "check_docker_available",
    "DEFAULT_IMAGE_NAME",
    "CONTAINER_SUT_DIR",
    "CONTAINER_SESSION_DIR",
    # Custom agent loader
    "load_custom_agents",
    "validate_agent_class",
    # Container mode utilities
    "is_container_mode",
    "get_session_dir",
    "get_container_workdir",
    # 工具函数
    "WORK_DIR",
    "load_env_file",
    "setup_logging",
    "ensure_directory",
    "has_sut_files",
    "get_env",
    "get_env_bool",
    # 日志系统
    "CommandResult",
    "LogManager",
]
