"""
HTTP Server System Under Test Implementation

HTTP/1.1 web server implementation that can be generated
and improved by AI agents. Evaluated via HTTP/1.1 conformance checks
and application-endpoint verification.
"""

import logging
import os
import socket
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any

from ..base import SystemUnderTest, SUTProcess

logger = logging.getLogger(__name__)


class HttpServerSUT(SystemUnderTest):
    """
    HTTP/1.1 Web Server System Under Test.

    This SUT type generates a web server that:
    - Implements HTTP/1.1 (RFC 9110/9112) request parsing and response construction
    - Supports routing, Keep-Alive, error handling, and standard headers
    - Targets application-level endpoints (plaintext, JSON, DB, fortunes, updates)

    Benchmarks: protocol conformance and application-endpoint verification
    """

    name = "http_server"
    description = "HTTP/1.1 web server"
    default_port = 8080

    def __init__(
        self,
        work_dir: Path,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(work_dir, config)

    def start(
        self,
        host: str = "127.0.0.1",
        port: Optional[int] = None,
        **kwargs
    ) -> Optional[SUTProcess]:
        """
        Start the HTTP server.

        Args:
            host: Host address to bind to
            port: Port to listen on (default: 8080)
            **kwargs: Additional arguments

        Returns:
            SUTProcess if started successfully, None otherwise
        """
        if port is None:
            port = self.config.get("port", self.default_port)

        # Check if port is already in use
        if self._check_port_in_use(host, port):
            logger.error(f"Port {port} is already in use")
            return None

        start_script = self.find_start_script()
        if not start_script:
            logger.error(f"No start script found in {self.work_dir}")
            return None

        logger.info(f"Found start script: {start_script}")

        try:
            log_file = kwargs.get("log_file") or self.work_dir / "server.log"
            uses_nohup = False

            # Determine how to run the script
            if start_script.suffix == ".sh":
                os.chmod(start_script, 0o755)
                # Check if script uses nohup
                try:
                    script_content = start_script.read_text()
                    if "nohup" in script_content:
                        uses_nohup = True
                        logger.info("Detected nohup in start script")
                except Exception:
                    pass
                cmd = ["bash", str(start_script)]
            else:
                cmd = ["python3", str(start_script)]

            logger.info(f"Starting HTTP server: {' '.join(cmd)}")
            env = {
                **os.environ,
                "HTTP_HOST": host,
                "HTTP_PORT": str(port),
            }

            log_file_handle = open(log_file, "w")
            try:
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(self.work_dir),
                    stdout=log_file_handle,
                    stderr=subprocess.STDOUT,
                    env=env,
                    start_new_session=True,
                )
            except Exception as e:
                log_file_handle.close()
                raise e

            # Wait for process to start
            time.sleep(2)

            sut_process = SUTProcess(
                process=proc,
                pid=proc.pid,
                host=host,
                port=port,
                log_file=log_file,
                log_file_handle=log_file_handle,
                uses_nohup=uses_nohup,
            )

            if uses_nohup:
                # For nohup scripts, check via port
                success, nohup_pid = self._detect_nohup_process(
                    host, port, log_file,
                    startup_patterns=[
                        "Server listening", "listening on", "server started",
                        "HTTP server started", "Accepting connections",
                        "ready to accept connections", "server ready",
                        "Serving on", "Started HTTP server",
                    ]
                )
                if success:
                    sut_process.nohup_pid = nohup_pid
                    self._process = sut_process
                    return sut_process
                else:
                    logger.error("HTTP server failed to start (nohup mode)")
                    sut_process.close_log_handle()
                    return None
            else:
                # Normal process - check if still running
                if proc.poll() is not None:
                    logger.error(f"HTTP server process exited immediately with code: {proc.returncode}")
                    sut_process.close_log_handle()
                    if log_file.exists():
                        content = log_file.read_text()[:1000]
                        logger.error(f"Log content:\n{content}")
                    return None

                self._process = sut_process
                logger.info(f"HTTP server started, PID: {proc.pid}")
                return sut_process

        except Exception as e:
            logger.error(f"Failed to start HTTP server: {e}")
            return None

    def check_ready(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        **kwargs
    ) -> bool:
        """
        Check if HTTP server is ready to accept connections.

        Tries a TCP connect first, then an HTTP GET request.

        Args:
            host: Host address
            port: Port number
            timeout: Maximum seconds to wait

        Returns:
            True if HTTP server is ready
        """
        logger.info(f"Waiting for HTTP server to be ready (max {timeout}s)...")

        for i in range(timeout):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    # Try a simple HTTP request
                    if self._try_http_check(host, port):
                        logger.info("HTTP server is ready (HTTP check passed)")
                        return True
                    # If HTTP check fails, accept port open
                    logger.info("HTTP server port is open")
                    return True
            except Exception as e:
                logger.debug(f"Port check error: {e}")

            time.sleep(1)
            if (i + 1) % 5 == 0:
                logger.info(f"Still waiting... ({i + 1}/{timeout})")

        logger.warning("HTTP server did not become ready in time")
        return False

    def stop(self) -> bool:
        """
        Stop the running HTTP server.

        Returns:
            True if stopped successfully
        """
        if self._process is None:
            return True

        proc = self._process
        result = proc.terminate()

        host = getattr(proc, "host", None)
        port = getattr(proc, "port", None)
        needs_cleanup = isinstance(host, str) and isinstance(port, int) and port > 0

        if needs_cleanup and self._check_port_in_use(host, port):
            logger.warning("HTTP server still listening on %s:%s after stop; trying fallback cleanup", host, port)
            self._kill_listener_on_port(host, port)
            if self._check_port_in_use(host, port):
                if self._cleanup_docker_by_port(port):
                    self._wait_for_port_release(host, port, timeout=10.0)
            if self._check_port_in_use(host, port):
                logger.error("HTTP server cleanup incomplete: %s:%s is still in use", host, port)
                result = False

        self._process = None
        return result

    # ------------------------------------------------------------------
    # Spec-file discovery helper
    # ------------------------------------------------------------------

    def _find_spec_files(self) -> list:
        """Find spec files under work_dir/spec (supports .md and .txt)."""
        spec_files: list = []
        spec_http_dir = self.work_dir / "spec" / "http_server"
        if spec_http_dir.is_dir():
            spec_files = sorted(
                str(p.relative_to(self.work_dir)).replace("\\", "/")
                for p in spec_http_dir.rglob("*")
                if p.is_file() and p.suffix in (".md", ".txt") and not p.name.startswith(".")
            )
        if not spec_files:
            spec_dir = self.work_dir / "spec"
            if spec_dir.is_dir():
                spec_files = sorted(
                    str(p.relative_to(self.work_dir)).replace("\\", "/")
                    for p in spec_dir.rglob("*")
                    if p.is_file() and p.suffix in (".md", ".txt") and not p.name.startswith(".")
                )
        return spec_files

    def _build_spec_guidance(self, item_number: int) -> str:
        """Build a spec-guidance paragraph referencing discovered spec files."""
        spec_files = self._find_spec_files()
        if not spec_files:
            return ""
        spec_examples = ", ".join(spec_files[:5])
        if len(spec_files) > 5:
            spec_examples += ", ..."
        return f"""{item_number}. **RFC / spec documents** are available under `./spec/` (e.g., {spec_examples}).
   - These are the authoritative references for protocol behaviour.
   - Locate relevant files by RFC number or keyword, then read only the sections you need for the current task.
   - Use the specs as design and compatibility targets; validate behaviour with runnable local tests.
   - If a spec passage conflicts with your actual test results, prioritise test evidence and document the deviation.
"""

    # ------------------------------------------------------------------
    # Prompts
    # ------------------------------------------------------------------

    def get_init_prompt(self) -> str:
        """
        Get the initialization prompt for creating an HTTP/1.1 web server.

        Returns:
            Initialization prompt string
        """
        spec_guidance = self._build_spec_guidance(9)

        return f"""Build a custom HTTP/1.1 web server implementation.

Execution strategy (important):
- This initialization step is only phase 1. Do NOT try to perfect everything in one shot.
- Deliver a runnable minimum implementation first (core HTTP/1.1 protocol + basic routing + start script), and leave advanced capabilities (database endpoints, template rendering) for later improvement iterations.
- When a requirement is not fully complete yet, implement the best practical subset now and structure code for incremental extension.

Requirements:
1. Use Python and do not depend on any existing HTTP server frameworks or libraries (e.g., no Flask, no Django, no http.server, no aiohttp). You may use the standard library and common packages.

2. **HTTP/1.1 Protocol requirements** (RFC 9110 / RFC 9112):
   - Parse HTTP/1.1 request line: method SP request-target SP HTTP-version CRLF
   - Parse request headers (field-name ":" OWS field-value OWS CRLF)
   - Construct valid HTTP/1.1 responses (status-line + headers + body)
   - Required response headers: Content-Length, Content-Type, Date (IMF-fixdate format per RFC 9110 §5.6.7), Server
   - Support GET, HEAD, POST methods; return 501 for unsupported methods
   - Return proper error responses: 400 (bad request), 404 (not found), 414 (URI too long), 501 (not implemented)
   - Connection management: Keep-Alive by default for HTTP/1.1, handle Connection: close (RFC 9112 §9.3)
   - Transfer-Encoding: chunked support for responses (RFC 9112 §7.1)
   - Robust parsing: handle malformed requests without crashing; defend against request-smuggling ambiguities (RFC 9112 §11.2)

3. **Routing and endpoints**:
   - `/plaintext` — return exactly `Hello, World!` with Content-Type: text/plain; charset=utf-8
   - `/json` — return `{{"message":"Hello, World!"}}` with Content-Type: application/json
   - `/` — return a simple welcome page or redirect to /plaintext

4. **Architecture requirements**:
   - Must support concurrent connections (multi-threading, select/poll/epoll, or asyncio)
   - Handle HTTP pipelining (multiple requests on a single connection)
   - Support at least 256 concurrent connections

5. **Robustness requirements**:
   - Handle `SIGTERM` and `SIGINT` for graceful shutdown and proper socket/port release
   - Implement solid exception handling so a single connection error does not crash the whole server
   - Handle slow clients, partial reads, and connection resets gracefully

6. **[CRITICAL] Startup script** — Create `start.sh` that reads configuration from environment variables:
   - `HTTP_HOST` — bind address (default: 0.0.0.0)
   - `HTTP_PORT` — HTTP/1.1 listening port (default: 8080)
   - **This is the MOST IMPORTANT deliverable. Without a working `start.sh`, the system CANNOT be tested at all and all benchmarks will fail.**
   - `start.sh` must be in the project root directory, must be executable, and must start the server in the foreground (or via nohup).
   - The server process started by `start.sh` must listen on the port specified by `HTTP_PORT`.
   - Do NOT delete, rename, or break `start.sh` under any circumstances.

7. **Performance targets** (not required for initialization, but design with these in mind):
   - The server will be stress-tested for requests/sec under high concurrency
   - Efficient I/O is important for later performance tests
   - Date header can be cached and updated every second (not per-request)

8. **Future progression** (do NOT implement now, but structure code for these):
   - Stage A: solid HTTP/1.1 protocol correctness and parser robustness
   - Stage B: stricter compliance and connection-lifecycle behavior
   - Stage C: stable application endpoints under concurrency and pipelining
   - Stage D: database-backed dynamic endpoints and data consistency
   - Stage E: performance, security hardening, and long-running stability
{spec_guidance}
10. PLAN.md requirements:
    Create a structured PLAN.md to guide future iterations. PLAN.md must follow a structured state-machine format.
    A. State Machine Rules
      - Allowed states: TODO | IN_PROGRESS | DONE | BLOCKED
      - Allowed transitions:
          TODO -> IN_PROGRESS -> DONE
          TODO/IN_PROGRESS -> BLOCKED -> IN_PROGRESS
          DONE -> TODO  (reopen on regression/bug found by external tests)
      - At any time, there must be at most ONE item marked IN_PROGRESS.
      - Every item must define acceptance_tests (runnable commands).
   B. Backlog Structure (use consistent structured fields)
      Each task must include:
      - id: unique identifier (e.g., P1-HTTP-001)
      - title:
      - state:
      - priority: P0 | P1 | P2
      - deps: [list of task ids]
      - acceptance_tests: [shell or Python commands]
      - notes: ...
   C. Phase 1 Constraint
      - PLAN.md should define a clear roadmap for later iterations across staged protocol, endpoint, database, and robustness goals.
      - Keep total tasks under 200 items.
      - Only one task should be marked IN_PROGRESS at initialization.
      - All Phase 1 deliverables must have concrete acceptance_tests.

11.{self.get_git_init_guidance()}
Please deliver Phase 1: a runnable minimal implementation + clear plan in PLAN.md for later iterations."""

    def get_improve_prompt(self, iteration: int, feedback: Optional[str] = None) -> str:
        """
        Get the improvement prompt for enhancing the HTTP server.

        Args:
            iteration: Current improvement iteration number
            feedback: Optional feedback from previous benchmarks

        Returns:
            Improvement prompt string
        """
        if feedback is None:
            feedback = self.read_feedback()

        spec_guidance = self._build_spec_guidance(5)

        prompt = f"""Improve the HTTP/1.1 web server implementation in the current directory.

Iteration strategy (important):
- Continue from the existing codebase and improve it incrementally; do not rewrite from scratch unless absolutely necessary.
- In later improvement, always:
    1. Read PLAN.md
    2. Select **EXACTLY ONE** the highest-priority TODO item
    3. Move it to IN_PROGRESS
    4. Implement minimally
    5. Run acceptance_tests
    6. Mark DONE or BLOCKED
- Keep the system runnable after this iteration.
- Include an "Iteration Log" section.
    Each entry must contain:
    - iteration id #{iteration}
    - selected task id
    - files changed
    - tests executed
    - result summary
    - follow-up tasks (if any)
- Do NOT:
   - Delete historical logs
   - Rewrite the whole plan
   - Expand scope beyond the selected task

**[CRITICAL] `start.sh` is the entry point used by the test runner to start the server. Without a working `start.sh` in the project root, NO benchmarks can run and ALL tests will fail. Never delete, rename, or break `start.sh`. After every change, verify that `bash start.sh` still starts the server correctly on the port specified by `HTTP_PORT`.**

This is improvement iteration #{iteration}. Please:
1. Analyze the current codebase and identify improvement opportunities.
2. Follow an incremental progression from protocol correctness to endpoint completeness, then to database-backed behavior, and finally to robustness/performance hardening.
3. Improve HTTP protocol compliance, stability, or correctness.
4. Design and write comprehensive regression tests, run them, and fix code defects based on observed results.
   - Cover malformed inputs and protocol edge cases
   - Cover response formatting and required headers
   - Cover connection lifecycle and concurrency behavior
   - Cover endpoint contract correctness (including database-backed endpoints when implemented)
{self.get_git_improve_guidance(iteration)}"""
        if spec_guidance:
            prompt += f"""{spec_guidance}
"""

        if feedback:
            brief_file = self.get_brief_summary_file()
            prompt += f"""6. Benchmark briefs are stored as `./last_brief/last_brief_i.txt`; the latest one is `{brief_file}` (lagging and potentially inaccurate).
Notes:
* The benchmark brief is not updated in real time and may be inconsistent with the current code state.
* Do not treat it as the only source of truth or optimize only for that report.
* Use current code analysis plus reproducible local tests (run by you in this iteration) to diagnose issues and validate fixes.
* If the brief conflicts with your actual test results, trust your actual test results and explain the discrepancy.
* Diagnose, modify code, run tests, and verify fixes based on your own executed test outputs. Build and run your own regression suite. Any conclusion must come from tests executed in this iteration; the brief is only a directional hint.
* PLAN sync rule (mandatory, minimal):
    - After reading `{brief_file}`, extract any failing behaviors/errors mentioned.
    - For each failure, find the most relevant task(s) in PLAN.md.
    - If any such task is currently marked DONE, reopen it by changing its state to TODO
Current benchmark feedback content:
```text
{feedback}
```
"""

        return prompt

    def find_start_script(self) -> Optional[Path]:
        """
        Find the HTTP server start script.

        Returns:
            Path to start script or None
        """
        possible_names = [
            "start.sh",
            "start.py",
            "server.py",
            "http_server.py",
            "main.py",
        ]

        for name in possible_names:
            script = self.work_dir / name
            if script.exists():
                return script

        py_files = list(self.work_dir.glob("*.py"))
        for f in py_files:
            if "server" in f.name.lower() or "http" in f.name.lower():
                return f

        if py_files:
            return py_files[0]

        return None

    def _try_http_check(self, host: str, port: int) -> bool:
        """Try a simple HTTP GET request to verify the server responds."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            request = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
            sock.sendall(request)
            response = sock.recv(1024)
            sock.close()
            # Check for any HTTP response
            return response.startswith(b"HTTP/")
        except Exception:
            return False


# Register the SUT
from ..registry import register_sut
register_sut("http_server", HttpServerSUT)
