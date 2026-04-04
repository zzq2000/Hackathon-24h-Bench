"""
System Under Test (SUT) Base Class

Defines the abstract interface that all system implementations must follow.
"""

import logging
import re
import signal
import socket
import subprocess
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class SUTProcess:
    """Represents a running system process."""

    process: Optional[subprocess.Popen] = None
    pid: Optional[int] = None
    host: str = "127.0.0.1"
    port: int = 0
    log_file: Optional[Path] = None
    log_file_handle: Optional[Any] = None  # File handle for log output
    uses_nohup: bool = False
    nohup_pid: Optional[int] = None
    extra_info: Dict[str, Any] = field(default_factory=dict)

    def close_log_handle(self) -> None:
        """Close the log file handle if open."""
        if self.log_file_handle is not None:
            try:
                self.log_file_handle.close()
                self.log_file_handle = None
            except Exception as e:
                logger.debug(f"Error closing log file handle: {e}")

    def is_running(self) -> bool:
        """Check if the process is still running."""
        if self.uses_nohup:
            if self.nohup_pid:
                try:
                    os.kill(self.nohup_pid, 0)
                    return True
                except (ProcessLookupError, OSError):
                    return False
            return False

        if self.process:
            return self.process.poll() is None
        return False

    def terminate(self, timeout: int = 10) -> bool:
        """
        Terminate the process gracefully.

        Args:
            timeout: Seconds to wait before force killing

        Returns:
            True if process was successfully terminated
        """
        result = False

        if self.uses_nohup:
            pid_to_kill = self.nohup_pid
            if not pid_to_kill:
                logger.warning("No nohup PID available for termination")
                self.close_log_handle()
                return False

            try:
                os.kill(pid_to_kill, signal.SIGTERM)
                for _ in range(timeout * 2):
                    try:
                        os.kill(pid_to_kill, 0)
                        time.sleep(0.5)
                    except ProcessLookupError:
                        logger.info(f"Process {pid_to_kill} terminated successfully")
                        result = True
                        break

                if not result:
                    # Force kill if still running
                    try:
                        os.kill(pid_to_kill, signal.SIGKILL)
                        logger.warning(f"Force killed process {pid_to_kill}")
                        result = True
                    except ProcessLookupError:
                        result = True

            except ProcessLookupError:
                logger.info(f"Process {pid_to_kill} already terminated")
                result = True
            except Exception as e:
                logger.error(f"Error terminating process {pid_to_kill}: {e}")
                result = False

            self.close_log_handle()
            return result

        if self.process and self.process.poll() is None:
            try:
                pid = getattr(self.process, "pid", None)
                if isinstance(pid, int) and pid > 0:
                    # Process is launched in its own session; terminate the whole group.
                    try:
                        os.killpg(pid, signal.SIGTERM)
                    except ProcessLookupError:
                        result = True
                    else:
                        deadline = time.time() + max(1, timeout)
                        while time.time() < deadline:
                            if self.process.poll() is not None:
                                result = True
                                break
                            time.sleep(0.2)

                        if not result:
                            try:
                                os.killpg(pid, signal.SIGKILL)
                                self.process.wait(timeout=2)
                                logger.warning("Force killed process group after timeout")
                                result = True
                            except ProcessLookupError:
                                result = True
                else:
                    self.process.terminate()
                    self.process.wait(timeout=timeout)
                    logger.info("Process terminated successfully")
                    result = True
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
                logger.warning("Force killed process after timeout")
                result = True
            except Exception as e:
                logger.error(f"Error terminating process: {e}")
                result = False

            self.close_log_handle()
            return result

        self.close_log_handle()
        return True


class SystemUnderTest(ABC):
    """
    Abstract base class for System Under Test implementations.

    A SUT represents a system that can be:
    - Started with specific configuration
    - Checked for readiness
    - Stopped gracefully
    - Described via prompts for AI agent initialization and improvement

    Subclasses must implement all abstract methods to define a specific
    system type (e.g., database, message queue, web server).

    Attributes:
        name: Unique identifier for this SUT type
        work_dir: Working directory containing the system code
        config: Configuration dictionary

    Example:
        >>> class DatabaseSUT(SystemUnderTest):
        ...     name = "database"
        ...
        ...     def start(self, config):
        ...         # Start the database server
        ...         pass
        ...
        ...     def check_ready(self):
        ...         # Check if database accepts connections
        ...         return True
        ...
        ...     def stop(self):
        ...         return True
    """

    # SUT type name, subclasses must override
    name: str = "base"

    # Human-readable description
    description: str = "Base System Under Test"

    # Default port for this system type (if applicable)
    default_port: int = 0
    brief_dir_name: str = "last_brief"
    brief_file_prefix: str = "last_brief_"
    brief_file_suffix: str = ".txt"

    def __init__(
        self,
        work_dir: Path,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the SUT.

        Args:
            work_dir: Working directory containing system code
            config: Optional configuration dictionary
        """
        self.work_dir = work_dir
        self.config = config or {}
        self._process: Optional[SUTProcess] = None
        self.last_ready_error: Optional[str] = None

    @property
    def is_running(self) -> bool:
        """Check if the system is currently running."""
        return self._process is not None and self._process.is_running()

    @abstractmethod
    def start(
        self,
        host: str = "127.0.0.1",
        port: Optional[int] = None,
        **kwargs
    ) -> Optional[SUTProcess]:
        """
        Start the system.

        Args:
            host: Host address to bind to
            port: Port to listen on (None for default/auto)
            **kwargs: Additional system-specific arguments

        Returns:
            SUTProcess if started successfully, None otherwise
        """
        pass

    @abstractmethod
    def check_ready(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        **kwargs
    ) -> bool:
        """
        Check if the system is ready to accept requests.

        Args:
            host: Host address
            port: Port number
            timeout: Maximum seconds to wait
            **kwargs: Additional system-specific arguments

        Returns:
            True if system is ready
        """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the running system gracefully.

        Returns:
            True if stopped successfully
        """
        pass

    @abstractmethod
    def get_init_prompt(self) -> str:
        """
        Get the initialization prompt for AI agents.

        This prompt describes what system to create from scratch.

        Returns:
            Initialization prompt string
        """
        pass

    @abstractmethod
    def get_improve_prompt(self, iteration: int, feedback: Optional[str] = None) -> str:
        """
        Get the improvement prompt for AI agents.

        Args:
            iteration: Current improvement iteration number
            feedback: Optional feedback from previous benchmarks

        Returns:
            Improvement prompt string
        """
        pass

    def find_start_script(self) -> Optional[Path]:
        """
        Find the start script in the working directory.

        Default implementation looks for common script names.
        Subclasses can override for specific patterns.

        Returns:
            Path to start script or None
        """
        # Common start script names
        possible_names = ["start.sh", "start.py", "server.py", "main.py"]

        for name in possible_names:
            script = self.work_dir / name
            if script.exists():
                return script

        # Look for any Python file with 'server' or 'main' in name
        py_files = list(self.work_dir.glob("*.py"))
        for f in py_files:
            if "server" in f.name.lower() or "main" in f.name.lower():
                return f

        # Return first Python file if any
        if py_files:
            return py_files[0]

        return None

    def has_implementation_files(self) -> bool:
        """
        Check if the working directory has implementation files.

        Default implementation checks for Python or shell scripts.
        Subclasses can override for specific requirements.

        Returns:
            True if implementation files exist
        """
        py_files = list(self.work_dir.glob("*.py"))
        sh_files = list(self.work_dir.glob("*.sh"))
        return len(py_files) > 0 or len(sh_files) > 0

    def get_connection_info(self) -> Dict[str, Any]:
        """
        Get connection information for the running system.

        Returns:
            Dictionary with connection details
        """
        if self._process:
            return {
                "host": self._process.host,
                "port": self._process.port,
                "pid": self._process.pid or self._process.nohup_pid,
                "running": self._process.is_running(),
            }
        return {}

    def get_brief_summary_dir(self) -> Path:
        """
        Get the path to the brief summary directory.

        Returns:
            Path to ./last_brief/
        """
        return self.work_dir / self.brief_dir_name

    def _extract_brief_index(self, file_path: Path) -> Optional[int]:
        """
        Extract numeric brief index from filename.

        Expected filename: last_brief_<i>.txt
        """
        pattern = (
            rf"^{re.escape(self.brief_file_prefix)}(\d+)"
            rf"{re.escape(self.brief_file_suffix)}$"
        )
        match = re.match(pattern, file_path.name)
        if not match:
            return None
        index = int(match.group(1))
        return index if index > 0 else None

    def _find_max_brief_index(self) -> int:
        """Find the maximum existing brief file index under ./last_brief/."""
        brief_dir = self.get_brief_summary_dir()
        if not brief_dir.is_dir():
            return 0

        max_index = 0
        for file_path in brief_dir.iterdir():
            if not file_path.is_file():
                continue
            index = self._extract_brief_index(file_path)
            if index and index > max_index:
                max_index = index
        return max_index

    def get_latest_brief_summary_file(self) -> Optional[Path]:
        """
        Get the latest brief summary file path.

        Returns:
            Path to ./last_brief/last_brief_<max_i>.txt, or legacy last_brief.txt
        """
        max_index = self._find_max_brief_index()
        if max_index > 0:
            return self.get_brief_summary_dir() / (
                f"{self.brief_file_prefix}{max_index}{self.brief_file_suffix}"
            )

        legacy_file = self.work_dir / "last_brief.txt"
        if legacy_file.exists():
            return legacy_file
        return None

    def get_next_brief_summary_file(self) -> Path:
        """
        Get next brief summary file path using max-index + 1.

        Returns:
            Path to ./last_brief/last_brief_<next_i>.txt
        """
        brief_dir = self.get_brief_summary_dir()
        brief_dir.mkdir(parents=True, exist_ok=True)
        next_index = self._find_max_brief_index() + 1
        return brief_dir / f"{self.brief_file_prefix}{next_index}{self.brief_file_suffix}"

    def get_brief_summary_file(self) -> Path:
        """
        Get a reference brief summary file path.

        Returns:
            Latest existing brief file if available, otherwise ./last_brief/last_brief_1.txt
        """
        latest_file = self.get_latest_brief_summary_file()
        if latest_file is not None:
            return latest_file
        return self.get_brief_summary_dir() / f"{self.brief_file_prefix}1{self.brief_file_suffix}"
    
    def get_spec_dir(self) -> Path:
        """
        Get the path to the system specification file.

        Returns:
            Path to spec directory
        """
        return self.work_dir / "spec"

    def read_feedback(self) -> str:
        """
        Read the latest feedback from the brief summary file.

        Returns:
            Feedback content or empty string
        """
        brief_file = self.get_latest_brief_summary_file()
        if brief_file and brief_file.exists():
            try:
                return brief_file.read_text(encoding="utf-8").strip()
            except Exception as e:
                logger.warning(f"Failed to read feedback file: {e}")
        return ""
    
    def read_spec_files(self) -> list:
        """
        Read the system specification from the spec directory.

        Returns:
            Specification content or empty string
        """
        spec_dir = self.get_spec_dir()
        if spec_dir.exists() and spec_dir.is_dir():
            spec_files = list(spec_dir.glob("*"))
            if spec_files:
                try:
                    return spec_files
                except Exception as e:
                    logger.warning(f"Failed to read spec file: {e}")
        return []

    def get_git_init_guidance(self) -> str:
        """Git guidance for init prompt."""
        return """[Version Control]
- Run `git init` and create a `.gitignore` (exclude __pycache__, *.pyc, data/, logs/, *.pid, etc.).
- After completing the initial implementation, stage all files and make an initial commit with a descriptive message (e.g., "iter #0: initial implementation with core functionality and start.sh").
"""

    def get_git_improve_guidance(self, iteration: int) -> str:
        """Git guidance for improve prompt, with iteration number for commit message format."""
        return f"""[Version Control — mandatory workflow]
- Before making any code changes, commit or stash any uncommitted work so you have a clean rollback point.
- Make small, focused commits after each meaningful change (e.g., after fixing a bug, adding a feature, or refactoring). Do NOT batch all changes into one giant commit at the end.
- Prefix commit messages with the iteration number: "iter #N: <description>" (e.g., "iter #{iteration}: fix NULL handling in WHERE clause").
- For large or risky changes (e.g., major refactoring, storage engine changes, protocol rewrites), create a feature branch first, implement and test on the branch, then merge back to main only after tests pass. If the branch breaks things, you can simply abandon it and return to main.
- After finishing all changes, run `git log --oneline -10` to review your commits for this iteration.
- If a change breaks the system (start.sh fails or tests regress), use `git diff` to identify the problem, and `git stash` or `git checkout -- <file>` to revert problematic changes. For larger rollbacks, use `git log` to find the last known-good commit and `git revert`.
"""

    def validate_config(self) -> List[str]:
        """
        Validate the SUT configuration.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        if not self.work_dir.exists():
            errors.append(f"Work directory does not exist: {self.work_dir}")
        return errors

    def _check_port_in_use(self, host: str, port: int) -> bool:
        """
        Check if a port is already in use.

        Args:
            host: Host address
            port: Port number

        Returns:
            True if port is in use
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def _get_pid_by_port(self, port: int) -> Optional[int]:
        """
        Get PID of process listening on a port.

        Args:
            port: Port number

        Returns:
            Process ID or None
        """
        # Try lsof first
        try:
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return int(result.stdout.strip().split('\n')[0])
        except Exception:
            pass

        # Try fuser as fallback
        try:
            result = subprocess.run(
                ["fuser", f"{port}/tcp"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split()
                if len(parts) > 1:
                    return int(parts[-1])
        except Exception:
            pass

        return None

    def _detect_nohup_process(
        self,
        host: str,
        port: int,
        log_file: Path,
        startup_patterns: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[int]]:
        """
        Detect nohup-started process via log file and port.

        Args:
            host: Host address
            port: Port number
            log_file: Path to log file
            startup_patterns: Patterns indicating successful startup

        Returns:
            (success, pid) tuple
        """
        if startup_patterns is None:
            startup_patterns = ["Server listening", "listening on", "started"]

        # Check log file for startup confirmation
        if log_file.exists():
            try:
                content = log_file.read_text()
                content_lower = content.lower()

                # Check for startup patterns
                for pattern in startup_patterns:
                    if pattern.lower() in content_lower:
                        logger.info(f"SUT started (detected via log: '{pattern}')")
                        pid = self._get_pid_by_port(port)
                        return True, pid

                # Check for error patterns
                if "error" in content_lower or "failed" in content_lower:
                    logger.error(f"SUT startup failed:\n{content[:1000]}")
                    return False, None
            except Exception:
                pass

        # Wait a bit more and check via port
        time.sleep(2)
        if self._check_port_in_use(host, port):
            logger.info("SUT port is open")
            pid = self._get_pid_by_port(port)
            return True, pid

        return False, None

    def _wait_for_port_release(self, host: str, port: int, timeout: float = 5.0) -> bool:
        """Wait until host:port is no longer reachable."""
        deadline = time.time() + max(0.2, timeout)
        while time.time() < deadline:
            if not self._check_port_in_use(host, port):
                return True
            time.sleep(0.2)
        return not self._check_port_in_use(host, port)

    def _kill_listener_on_port(self, host: str, port: int, timeout: float = 5.0) -> bool:
        """Best-effort kill of the process listening on a port."""
        pid = self._get_pid_by_port(port)
        if not isinstance(pid, int) or pid <= 1:
            return not self._check_port_in_use(host, port)

        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            return not self._check_port_in_use(host, port)
        except Exception as e:
            logger.warning(f"Failed to SIGTERM pid {pid} on port {port}: {e}")
            return False

        if self._wait_for_port_release(host, port, timeout=timeout):
            return True

        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except Exception as e:
            logger.warning(f"Failed to SIGKILL pid {pid} on port {port}: {e}")
            return False

        return self._wait_for_port_release(host, port, timeout=2.0)

    def _cleanup_docker_by_port(self, port: int) -> bool:
        """
        Best-effort cleanup of Docker containers publishing the given TCP port.
        Returns True if at least one container was cleaned up.
        """
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"publish={port}", "--format", "{{.ID}}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
        except FileNotFoundError:
            return False
        except Exception as e:
            logger.warning(f"Docker detection failed for port {port}: {e}")
            return False

        if result.returncode != 0:
            logger.warning(f"docker ps failed for port {port}: {result.stderr.strip()}")
            return False

        container_ids = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if not container_ids:
            return False

        cleaned = False
        for cid in container_ids:
            try:
                subprocess.run(["docker", "stop", cid], capture_output=True, text=True, timeout=20)
                subprocess.run(["docker", "rm", "-f", cid], capture_output=True, text=True, timeout=20)
                cleaned = True
            except Exception as e:
                logger.warning(f"Failed to stop/remove docker container {cid}: {e}")
        return cleaned
