"""
Message Queue System Under Test Implementation

AMQP 0.9.1 message queue implementation that can be generated
and improved by AI agents.
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


class MessageQueueSUT(SystemUnderTest):
    """
    AMQP 0.9.1 Message Queue System Under Test.

    This SUT type generates a message queue broker that:
    - Implements the AMQP 0.9.1 wire protocol
    - Supports exchanges (direct, fanout, topic), queues, and bindings
    - Provides connection/channel multiplexing
    - Includes message persistence and acknowledgments
    - Supports publisher confirms

    Evaluated via external AMQP protocol conformance and throughput benchmarks.
    """

    name = "message_queue"
    description = "AMQP 0.9.1 message queue"
    default_port = 5672

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
        Start the message queue server.

        Args:
            host: Host address to bind to
            port: Port to listen on (default: 5672)
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

            logger.info(f"Starting message queue: {' '.join(cmd)}")
            env = {**os.environ, "MQ_HOST": host, "MQ_PORT": str(port)}

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
                        "Server listening", "listening on", "broker started",
                        "AMQP server started", "Accepting connections",
                        "ready to accept connections", "server ready",
                    ]
                )
                if success:
                    sut_process.nohup_pid = nohup_pid
                    self._process = sut_process
                    return sut_process
                else:
                    logger.error("Message queue failed to start (nohup mode)")
                    sut_process.close_log_handle()
                    return None
            else:
                # Normal process - check if still running
                if proc.poll() is not None:
                    logger.error(f"Message queue process exited immediately with code: {proc.returncode}")
                    sut_process.close_log_handle()
                    if log_file.exists():
                        content = log_file.read_text()[:1000]
                        logger.error(f"Log content:\n{content}")
                    return None

                self._process = sut_process
                logger.info(f"Message queue started, PID: {proc.pid}")
                return sut_process

        except Exception as e:
            logger.error(f"Failed to start message queue: {e}")
            return None

    def check_ready(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        **kwargs
    ) -> bool:
        """
        Check if message queue is ready to accept connections.

        Args:
            host: Host address
            port: Port number
            timeout: Maximum seconds to wait

        Returns:
            True if message queue is ready
        """
        logger.info(f"Waiting for message queue to be ready (max {timeout}s)...")

        for i in range(timeout):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    # Try a simple protocol check if available
                    if self._try_protocol_check(host, port):
                        logger.info("Message queue is ready")
                        return True
                    # If no protocol check, just accept port open
                    logger.info("Message queue port is open")
                    return True
            except Exception as e:
                logger.debug(f"Port check error: {e}")

            time.sleep(1)
            if (i + 1) % 5 == 0:
                logger.info(f"Still waiting... ({i + 1}/{timeout})")

        logger.warning("Message queue did not become ready in time")
        return False

    def stop(self) -> bool:
        """
        Stop the running message queue server.

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
            logger.warning("Message queue still listening on %s:%s after stop; trying fallback cleanup", host, port)
            self._kill_listener_on_port(host, port)
            if self._check_port_in_use(host, port):
                if self._cleanup_docker_by_port(port):
                    self._wait_for_port_release(host, port, timeout=10.0)
            if self._check_port_in_use(host, port):
                logger.error("Message queue cleanup incomplete: %s:%s is still in use", host, port)
                result = False

        self._process = None
        return result

    def _find_spec_files(self) -> list:
        """Find spec files under work_dir/spec (supports .md and .txt)."""
        spec_files: list = []
        spec_mq_dir = self.work_dir / "spec" / "message_queue"
        if spec_mq_dir.is_dir():
            spec_files = sorted(
                str(p.relative_to(self.work_dir)).replace("\\", "/")
                for p in spec_mq_dir.rglob("*")
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
        spec_examples = ", ".join(spec_files[:3])
        if len(spec_files) > 3:
            spec_examples += ", ..."
        return f"""{item_number}. Additional implementation spec docs are available under `./spec` (e.g., {spec_examples}).
   - First locate relevant files by feature/keyword, then read only the sections needed for this iteration.
   - Use these specs as design/compatibility targets.
   - Do not treat spec docs as the only source of truth; validate behavior with runnable local tests.
   - If a spec conflicts with executable test evidence, prioritize test evidence and document the deviation.
"""

    def get_init_prompt(self) -> str:
        """
        Get the initialization prompt for creating an AMQP 0.9.1 message queue broker.

        Returns:
            Initialization prompt string
        """
        spec_guidance = self._build_spec_guidance(10)

        return f"""Build a custom AMQP 0.9.1 message queue broker implementation.

Execution strategy (important):
- This initialization step is only phase 1. Do NOT try to perfect everything in one shot.
- Deliver a runnable minimum implementation first (core AMQP 0.9.1 protocol + basic exchange/queue/publish/consume + start script), and leave advanced capabilities for later improvement iterations.
- When a requirement is not fully complete yet, implement the best practical subset now and structure code for incremental extension.

Requirements:
1. Use Python and do not depend on any existing message queue server libraries (e.g., no RabbitMQ, no ActiveMQ). You may use the standard library and common packages.

2. **Protocol requirements**:
   - **Must implement the AMQP 0.9.1 wire protocol** (reference the spec under `./spec/` if available)
   - Implement the binary frame format: METHOD, HEADER, BODY, and HEARTBEAT frame types
   - Support connection negotiation: connection.start / start-ok / tune / tune-ok / open / open-ok / close / close-ok
   - Support channel multiplexing: channel.open / open-ok / close / close-ok
   - Core entities:
     * **Exchanges**: direct, fanout, topic exchange types
     * **Queues**: durable, auto-delete, exclusive queue properties
     * **Bindings**: queue-to-exchange and exchange-to-exchange bindings with routing keys
   - Standard pre-declared exchanges: `amq.direct`, `amq.fanout`, `amq.topic`, and default exchange `""` (empty string, direct type)

3. **Required AMQP operations** (implement at minimum):
   - `queue.declare` / `queue.delete` / `queue.bind` / `queue.unbind` / `queue.purge`
   - `exchange.declare` / `exchange.delete`
   - `basic.publish` / `basic.consume` / `basic.get` / `basic.ack` / `basic.nack` / `basic.reject`
   - `basic.cancel` / `basic.qos`
   - `confirm.select` (publisher confirms)
   - `basic.recover`
   - `tx.select` / `tx.commit` / `tx.rollback` (transactions)

4. **Message handling**:
   - Support message properties (content-type, delivery-mode, headers, etc.)
   - Consumer acknowledgment modes (auto-ack and manual ack)
   - Publisher confirms mode (confirm.select + basic.ack/nack back to publisher)
   - Message persistence (delivery-mode=2)
   - Basic QoS / prefetch (basic.qos with prefetch_count)

5. **Architecture requirements**:
   - Must support concurrent connections (multi-threading or asyncio)
   - Implement proper AMQP frame parsing and serialization
   - Handle HEARTBEAT frames for connection keepalive
   - Support multiple channels per connection

6. **Robustness requirements**:
   - Handle `SIGTERM` and `SIGINT` for graceful shutdown and proper socket/port release
   - Implement solid exception handling so a single connection error does not crash the whole server
   - Properly handle connection and channel errors per AMQP spec (close with error codes)

7. **[CRITICAL] Create a startup script `start.sh`** and read host/port from environment variables `MQ_HOST`/`MQ_PORT`. Default port: 5672.
   - **This is the MOST IMPORTANT deliverable. Without a working `start.sh`, the system CANNOT be tested at all and all benchmarks will fail.**
   - `start.sh` must be in the project root directory, must be executable, and must start the broker in the foreground (or via nohup).
   - The broker process started by `start.sh` must listen on the port specified by `MQ_PORT`.
   - Do NOT delete, rename, or break `start.sh` under any circumstances.

8. Default credentials: guest/guest (as per AMQP convention).
9. **Future progression** (do NOT implement now, but structure code for these):
   - Stage A: core AMQP 0.9.1 protocol correctness (connection/channel lifecycle, frame parsing)
   - Stage B: exchange routing (direct, fanout, topic), queue binding, and consumer acknowledgment
   - Stage C: publisher confirms, QoS/prefetch, and transactions (tx.select/commit/rollback)
   - Stage D: throughput optimization under concurrent publishers/consumers
   - Stage E: message persistence, durability guarantees, and long-running stability
{spec_guidance}
11. PLAN.md requirements:
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
      - id: unique identifier (e.g., P1-PROTO-001)
      - title:
      - state:
      - priority: P0 | P1 | P2
      - deps: [list of task ids]
      - acceptance_tests: [shell or Python commands]
      - notes: ...
   C. Phase 1 Constraint
      - PLAN.md should define a clear roadmap for later iterations.
      - Keep total tasks under 200 items.
      - Only one task should be marked IN_PROGRESS at initialization.
      - All Phase 1 deliverables must have concrete acceptance_tests.

12.{self.get_git_init_guidance()}

Please deliver Phase 1: a runnable minimal implementation + clear plan in PLAN.md for later iterations."""

    def get_improve_prompt(self, iteration: int, feedback: Optional[str] = None) -> str:
        """
        Get the improvement prompt for enhancing the AMQP 0.9.1 message queue broker.

        Args:
            iteration: Current improvement iteration number
            feedback: Optional feedback from previous benchmarks

        Returns:
            Improvement prompt string
        """
        if feedback is None:
            feedback = self.read_feedback()

        spec_guidance = self._build_spec_guidance(5)

        prompt = f"""Improve the AMQP 0.9.1 message queue broker implementation in the current directory.

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

**[CRITICAL] `start.sh` is the entry point used by the test runner to start the broker. Without a working `start.sh` in the project root, NO benchmarks can run and ALL tests will fail. Never delete, rename, or break `start.sh`. After every change, verify that `bash start.sh` still starts the broker correctly on the port specified by `MQ_PORT`.**

This is improvement iteration #{iteration}. Please:
1. Analyze the current codebase and identify improvement opportunities.
2. Improve AMQP 0.9.1 protocol compliance, stability, or correctness.
3. Target full AMQP 0.9.1 protocol compliance: prioritize correct frame handling, exchange routing, consumer acknowledgment, and connection lifecycle.
4. Design and write comprehensive test cases, run them, and fix code defects based on observed results.
   - Connection open/close lifecycle test
   - Channel multiplexing test
   - Exchange declare and message routing test (direct, fanout, topic)
   - Queue declare, bind, consume, and ack test
   - Publisher confirms test
   - Basic.get (synchronous get) test
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
        Find the message queue start script.

        Returns:
            Path to start script or None
        """
        possible_names = [
            "start.sh",
            "start.py",
            "broker.py",
            "server.py",
            "mq_server.py",
            "main.py",
        ]

        for name in possible_names:
            script = self.work_dir / name
            if script.exists():
                return script

        py_files = list(self.work_dir.glob("*.py"))
        for f in py_files:
            if "server" in f.name.lower() or "broker" in f.name.lower():
                return f

        if py_files:
            return py_files[0]

        return None

    def _try_protocol_check(self, host: str, port: int) -> bool:
        """Try a simple protocol check."""
        # This could be extended to send a simple request
        # For now, just check if we can connect
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((host, port))
            sock.close()
            return True
        except Exception:
            return False


# Register the SUT
from ..registry import register_sut
register_sut("message_queue", MessageQueueSUT)
