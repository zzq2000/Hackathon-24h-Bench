"""
Docker runner module for containerized agent execution.

Provides DockerAgentRunner class to run code agents in Docker containers
for improved security and isolation.
"""

import os
import logging
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any

from .utils import get_env, get_env_bool

logger = logging.getLogger(__name__)

# Default Docker image name
DEFAULT_IMAGE_NAME = "code-agent-controller:latest"

# Container paths
CONTAINER_SUT_DIR = "/workspace/database"
CONTAINER_SESSION_DIR = "/workspace/sessions"
CONTAINER_CUSTOM_AGENTS_DIR = "/workspace/custom_agents"


class DockerAgentRunner:
    """
    Runner for executing code agents inside Docker containers.

    This class handles building Docker run commands, managing volume mounts,
    passing environment variables, and setting security options.

    Attributes:
        image_name: Docker image name to use
        sut_dir: Host path to SUT working directory
        session_dir: Host path to session files directory
        custom_agents_dir: Host path to custom agents directory (optional)
        container_name_prefix: Prefix for container names
        system_type: Type of system (database, message_queue)
    """

    def __init__(
        self,
        sut_dir: Path,
        session_dir: Optional[Path] = None,
        custom_agents_dir: Optional[Path] = None,
        image_name: str = DEFAULT_IMAGE_NAME,
        container_name_prefix: str = "agent-controller",
        system_type: str = "database",
    ):
        """
        Initialize Docker runner.

        Args:
            sut_dir: Host path to SUT working directory
            session_dir: Host path to session files directory
            custom_agents_dir: Optional path to custom agents directory
            image_name: Docker image name
            container_name_prefix: Prefix for container naming
            system_type: Type of system (database, message_queue)
        """
        self.sut_dir = Path(sut_dir).resolve()
        self.session_dir = Path(session_dir).resolve() if session_dir else self.sut_dir.parent / ".agent_sessions"
        self.custom_agents_dir = Path(custom_agents_dir).resolve() if custom_agents_dir else None
        self.image_name = image_name
        self.container_name_prefix = container_name_prefix
        self.system_type = system_type

    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.sut_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        if self.custom_agents_dir:
            self.custom_agents_dir.mkdir(parents=True, exist_ok=True)

    def _get_volume_mounts(self) -> List[str]:
        """
        Get volume mount arguments for Docker.

        Returns:
            List of -v arguments for Docker run
        """
        container_workdir = f"/workspace/{self.system_type}"
        mounts = [
            "-v", f"{self.sut_dir}:{container_workdir}:rw",
            "-v", f"{self.session_dir}:{CONTAINER_SESSION_DIR}:rw",
        ]

        # Sync host timezone into container
        localtime = Path("/etc/localtime")
        if localtime.exists():
            mounts.extend(["-v", "/etc/localtime:/etc/localtime:ro"])

        if self.custom_agents_dir and self.custom_agents_dir.exists():
            mounts.extend([
                "-v", f"{self.custom_agents_dir}:{CONTAINER_CUSTOM_AGENTS_DIR}:ro"
            ])

        return mounts

    def _get_env_vars(
        self,
        agent_type: str,
        model: Optional[str] = None,
        extra_env: Optional[Dict[str, str]] = None,
    ) -> List[str]:
        """
        Get environment variable arguments for Docker.

        Args:
            agent_type: Type of agent (codex, claude, gemini, kimi, opencode, qwen, grok)
            model: Optional model name
            extra_env: Additional environment variables

        Returns:
            List of -e arguments for Docker run
        """
        env_args = [
            "-e", "CONTAINER_MODE=true",
            "-e", f"SESSION_DIR={CONTAINER_SESSION_DIR}",
        ]
        emitted_env_keys = {"CONTAINER_MODE", "SESSION_DIR"}

        def _append_env(key: str, value: Optional[str]) -> None:
            if not key or not value:
                return
            if key in emitted_env_keys:
                return
            emitted_env_keys.add(key)
            env_args.extend(["-e", f"{key}={value}"])

        # Sync host timezone
        tz = os.environ.get("TZ")
        if not tz:
            try:
                tz = Path("/etc/timezone").read_text().strip()
            except OSError:
                try:
                    tz = os.readlink("/etc/localtime").split("zoneinfo/", 1)[1]
                except (OSError, IndexError):
                    tz = ""
        if tz:
            _append_env("TZ", tz)

        # Use ProviderRegistry to determine which env vars to pass
        try:
            from .providers import ProviderRegistry
            registry = ProviderRegistry.get_instance()
            keys_to_pass = registry.get_all_env_keys_for_agent(agent_type.lower())
        except Exception:
            # Fallback: pass common keys if registry is not available
            keys_to_pass = []

        # Also include agent-specific env vars not covered by provider registry
        _agent_extra_env_keys = {
            "codex": ["CODEX_BYPASS_SANDBOX"],
            "claude": [
                "CLAUDE_DANGEROUSLY_SKIP_PERMISSIONS",
                "CLAUDE_PROVIDER",
                "ANTHROPIC_MODEL",
                "ANTHROPIC_DEFAULT_OPUS_MODEL",
                "ANTHROPIC_DEFAULT_SONNET_MODEL",
            ],
            "gemini": ["GEMINI_SANDBOX_MODE", "GEMINI_APPROVAL_MODE"],
            "kimi": [
                "KIMI_THINKING",
                "KIMI_MODEL_NAME",
                "KIMI_MODEL_MAX_CONTEXT_SIZE",
                "KIMI_MODEL_CAPABILITIES",
                "KIMI_SHARE_DIR",
            ],
            "opencode": ["OPENCODE_API_KEY", "OPENCODE_APPROVAL_MODE", "OPENCODE_PERMISSION"],
            "qwen": ["QWEN_APPROVAL_MODE"],
            "grok": [],
            "cline": ["CLINE_PROVIDER", "CLINE_VERBOSE", "CLINE_JSON_OUTPUT"],
        }
        for key in _agent_extra_env_keys.get(agent_type.lower(), []):
            if key not in keys_to_pass:
                keys_to_pass.append(key)

        seen_keys = set()
        for key in keys_to_pass:
            if key in seen_keys:
                continue
            seen_keys.add(key)
            if model and key == "CODE_AGENT_MODEL":
                continue
            value = os.environ.get(key)
            if value:
                _append_env(key, value)

        # Pass model environment variables
        if model:
            _append_env("CODE_AGENT_MODEL", model)

        # Agent-specific model environment variables
        model_env_keys = [
            "CODE_AGENT_MODEL",
            "CODEX_MODEL",
            "CLAUDE_MODEL",
            "GEMINI_MODEL",
            "KIMI_MODEL",
            "OPENCODE_MODEL",
            "QWEN_MODEL",
            "GROK_MODEL",
            "CLINE_MODEL",
        ]
        for key in model_env_keys:
            value = os.environ.get(key)
            if value and not (model and key == "CODE_AGENT_MODEL"):
                _append_env(key, value)

        # Controller runtime controls
        control_env_keys = [
            "CODE_AGENT_WAIT_TIME",
            "CODE_AGENT_MAX_RETRIES",
            "CODE_AGENT_COMMAND_TIMEOUT",
            "AGENT_WAIT_TIME",
            "AGENT_MAX_RETRIES",
            "AGENT_COMMAND_TIMEOUT",
        ]
        for key in control_env_keys:
            value = os.environ.get(key)
            if value and value.strip():
                _append_env(key, value.strip())

        # Custom agents directory
        if self.custom_agents_dir:
            _append_env("CUSTOM_AGENTS_DIR", CONTAINER_CUSTOM_AGENTS_DIR)

        # Pass system type
        _append_env("SYSTEM_TYPE", self.system_type)

        # Extra environment variables
        if extra_env:
            for key, value in extra_env.items():
                _append_env(key, value)

        return env_args

    def _get_security_opts(self) -> List[str]:
        """
        Get security options for Docker.

        Returns:
            List of security-related arguments
        """
        return [
            "--security-opt", "no-new-privileges:true",
            "--cap-drop", "ALL",
            "--cap-add", "NET_BIND_SERVICE",
        ]

    def _get_user_mapping(self) -> List[str]:
        """
        Get user mapping arguments to match host user.

        Returns:
            List of user-related arguments
        """
        uid = os.getuid()
        gid = os.getgid()
        return ["--user", f"{uid}:{gid}"]

    def build_image(
        self,
        dockerfile_path: Optional[Path] = None,
        context_path: Optional[Path] = None,
        build_args: Optional[Dict[str, str]] = None,
    ) -> bool:
        """
        Build the Docker image.

        Args:
            dockerfile_path: Path to Dockerfile (default: Dockerfile.agents)
            context_path: Build context path (default: current directory)
            build_args: Build arguments

        Returns:
            True if build succeeded
        """
        from .utils import WORK_DIR

        dockerfile = dockerfile_path or (WORK_DIR / "Dockerfile.agents")
        context = context_path or WORK_DIR

        cmd = [
            "docker", "build",
            "-f", str(dockerfile),
            "-t", self.image_name,
        ]

        # Add build args
        if build_args:
            for key, value in build_args.items():
                cmd.extend(["--build-arg", f"{key}={value}"])

        # Add UID/GID build args for user mapping
        cmd.extend([
            "--build-arg", f"USER_UID={os.getuid()}",
            "--build-arg", f"USER_GID={os.getgid()}",
        ])

        cmd.append(str(context))

        logger.info(f"Building Docker image: {self.image_name}")
        logger.debug(f"Build command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )
            if result.returncode == 0:
                logger.info(f"Docker image built successfully: {self.image_name}")
                return True
            else:
                logger.error(f"Docker build failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("Docker build timed out")
            return False
        except Exception as e:
            logger.error(f"Docker build error: {e}")
            return False

    def image_exists(self) -> bool:
        """
        Check if Docker image exists.

        Returns:
            True if image exists
        """
        try:
            result = subprocess.run(
                ["docker", "image", "inspect", self.image_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0
        except Exception:
            return False

    def run_agent(
        self,
        agent_type: str,
        model: Optional[str] = None,
        wait_time: int = 30,
        max_iterations: int = 0,
        skip_init: bool = False,
        init_only: bool = False,
        detach: bool = False,
        extra_args: Optional[List[str]] = None,
    ) -> bool:
        """
        Run agent in Docker container.

        Args:
            agent_type: Type of agent (codex, claude, gemini, kimi, opencode, qwen, grok)
            model: Optional model name
            wait_time: Wait time between iterations
            max_iterations: Maximum iterations (0 = unlimited)
            skip_init: Skip initialization
            init_only: Only initialize, don't run improvement loop
            detach: Run container in detached mode
            extra_args: Additional arguments to pass to controller

        Returns:
            True if execution succeeded
        """
        self._ensure_directories()

        container_name = f"{self.container_name_prefix}-{agent_type}"

        # Build Docker run command
        cmd = ["docker", "run"]

        if detach:
            cmd.append("-d")
            cmd.extend(["--name", container_name])
        else:
            cmd.append("--rm")

        # Add volume mounts
        cmd.extend(self._get_volume_mounts())

        # Add environment variables
        cmd.extend(self._get_env_vars(agent_type, model))

        # Add user mapping
        cmd.extend(self._get_user_mapping())

        # Add security options
        cmd.extend(self._get_security_opts())

        # Add image name
        cmd.append(self.image_name)

        # Add controller arguments
        container_workdir = f"/workspace/{self.system_type}"
        cmd.extend(["--agent", agent_type])
        cmd.extend(["--sut-dir", container_workdir])
        cmd.extend(["--wait-time", str(wait_time)])

        if model:
            cmd.extend(["--model", model])

        if max_iterations > 0:
            cmd.extend(["--max-iterations", str(max_iterations)])

        if skip_init:
            cmd.append("--skip-init")

        if init_only:
            cmd.append("--init-only")

        if extra_args:
            cmd.extend(extra_args)

        logger.info(f"Starting Docker container for agent: {agent_type}")
        logger.debug(f"Docker command: {' '.join(cmd)}")

        try:
            if detach:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode == 0:
                    container_id = result.stdout.strip()
                    logger.info(f"Container started: {container_id[:12]}")
                    return True
                else:
                    logger.error(f"Failed to start container: {result.stderr}")
                    return False
            else:
                # Run interactively
                result = subprocess.run(cmd)
                return result.returncode == 0

        except subprocess.TimeoutExpired:
            logger.error("Docker run timed out")
            return False
        except KeyboardInterrupt:
            logger.info("Interrupted, stopping container...")
            self.stop_container(agent_type)
            return False
        except Exception as e:
            logger.error(f"Docker run error: {e}")
            return False

    def stop_container(self, agent_type: str) -> bool:
        """
        Stop a running container.

        Args:
            agent_type: Type of agent

        Returns:
            True if stopped successfully
        """
        container_name = f"{self.container_name_prefix}-{agent_type}"

        try:
            # Stop container
            result = subprocess.run(
                ["docker", "stop", container_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                logger.info(f"Container stopped: {container_name}")

            # Remove container
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return True

        except Exception as e:
            logger.error(f"Error stopping container: {e}")
            return False

    def get_container_logs(
        self,
        agent_type: str,
        follow: bool = False,
        tail: Optional[int] = None,
    ) -> Optional[str]:
        """
        Get logs from a container.

        Args:
            agent_type: Type of agent
            follow: Follow log output
            tail: Number of lines to show from end

        Returns:
            Log output or None if failed
        """
        container_name = f"{self.container_name_prefix}-{agent_type}"

        cmd = ["docker", "logs"]
        if follow:
            cmd.append("-f")
        if tail:
            cmd.extend(["--tail", str(tail)])
        cmd.append(container_name)

        try:
            if follow:
                subprocess.run(cmd)
                return None
            else:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return result.stdout + result.stderr

        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return None

    def is_container_running(self, agent_type: str) -> bool:
        """
        Check if container is running.

        Args:
            agent_type: Type of agent

        Returns:
            True if container is running
        """
        container_name = f"{self.container_name_prefix}-{agent_type}"

        try:
            result = subprocess.run(
                ["docker", "ps", "-q", "-f", f"name={container_name}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return bool(result.stdout.strip())
        except Exception:
            return False


def check_docker_available() -> bool:
    """
    Check if Docker is available on the system.

    Returns:
        True if Docker is available
    """
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            logger.debug(f"Docker available: {result.stdout.strip()}")
            return True
        return False
    except FileNotFoundError:
        logger.error("Docker not found. Please install Docker.")
        return False
    except Exception as e:
        logger.error(f"Error checking Docker: {e}")
        return False
