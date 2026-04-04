"""
Redis KV Store System Under Test Implementation

Redis-compatible in-memory KV store implementation that can be generated
and improved by AI agents. Evaluated via TCL tests, redis-benchmark,
YCSB, and memtier_benchmark.
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


class RedisKVStoreSUT(SystemUnderTest):
    """
    Redis-compatible KV Store System Under Test.

    This SUT type generates a Redis-compatible in-memory KV store that:
    - Implements the RESP2 wire protocol
    - Supports core Redis data structures (strings, lists, hashes, sets, sorted sets)
    - Provides persistence (RDB/AOF), transactions, pipelining
    - Supports Pub/Sub and SCAN family commands

    Evaluated via external Redis protocol conformance tests and workload benchmarks.
    """

    name = "redis_kvstore"
    description = "Redis-compatible KV store"
    default_port = 6379

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
        Start the Redis-compatible KV store server.

        Args:
            host: Host address to bind to
            port: Port to listen on (default: 6379)
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

            logger.info(f"Starting Redis KV store: {' '.join(cmd)}")
            env = {**os.environ, "REDIS_HOST": host, "REDIS_PORT": str(port)}

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
                        "Redis server started", "Accepting connections",
                        "ready to accept connections", "server ready",
                        "Ready to accept connections",
                    ]
                )
                if success:
                    sut_process.nohup_pid = nohup_pid
                    self._process = sut_process
                    return sut_process
                else:
                    logger.error("Redis KV store failed to start (nohup mode)")
                    sut_process.close_log_handle()
                    return None
            else:
                # Normal process - check if still running
                if proc.poll() is not None:
                    logger.error(f"Redis KV store process exited immediately with code: {proc.returncode}")
                    sut_process.close_log_handle()
                    if log_file.exists():
                        content = log_file.read_text()[:1000]
                        logger.error(f"Log content:\n{content}")
                    return None

                self._process = sut_process
                logger.info(f"Redis KV store started, PID: {proc.pid}")
                return sut_process

        except Exception as e:
            logger.error(f"Failed to start Redis KV store: {e}")
            return None

    def check_ready(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        **kwargs
    ) -> bool:
        """
        Check if Redis KV store is ready to accept connections.

        Uses TCP connect check (no RESP protocol handshake required).

        Args:
            host: Host address
            port: Port number
            timeout: Maximum seconds to wait

        Returns:
            True if KV store is ready
        """
        logger.info(f"Waiting for Redis KV store to be ready (max {timeout}s)...")

        for i in range(timeout):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    # Try a PING check if possible
                    if self._try_resp_ping(host, port):
                        logger.info("Redis KV store is ready (PING OK)")
                        return True
                    # If PING fails, accept port open
                    logger.info("Redis KV store port is open")
                    return True
            except Exception as e:
                logger.debug(f"Port check error: {e}")

            time.sleep(1)
            if (i + 1) % 5 == 0:
                logger.info(f"Still waiting... ({i + 1}/{timeout})")

        logger.warning("Redis KV store did not become ready in time")
        return False

    def stop(self) -> bool:
        """
        Stop the running Redis KV store server.

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
            logger.warning("Redis KV store still listening on %s:%s after stop; trying fallback cleanup", host, port)
            self._kill_listener_on_port(host, port)
            if self._check_port_in_use(host, port):
                if self._cleanup_docker_by_port(port):
                    self._wait_for_port_release(host, port, timeout=10.0)
            if self._check_port_in_use(host, port):
                logger.error("Redis KV store cleanup incomplete: %s:%s is still in use", host, port)
                result = False

        self._process = None
        return result

    def _find_spec_files(self) -> list:
        """Find spec files under work_dir/spec (supports .md and .txt)."""
        spec_files: list = []
        spec_redis_dir = self.work_dir / "spec" / "redis_kvstore"
        if spec_redis_dir.is_dir():
            spec_files = sorted(
                str(p.relative_to(self.work_dir)).replace("\\", "/")
                for p in spec_redis_dir.rglob("*")
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
   - Expect some spec pages to describe broader or newer Redis behavior than the local benchmark target.
   - Ignore out-of-scope material unless executable local tests require it (for example RESP3, ACL/AUTH, CLUSTER, EVAL/EVALSHA, module commands, or newer admin fields).
   - Do not treat spec docs as the only source of truth; validate behavior with runnable local tests.
   - If a spec conflicts with executable test evidence, prioritize test evidence and document the deviation.
"""

    def get_init_prompt(self) -> str:
        """
        Get the initialization prompt for creating a Redis-compatible KV store.

        Returns:
            Initialization prompt string
        """
        spec_guidance = self._build_spec_guidance(10)

        return f"""Build a custom Redis-compatible in-memory KV store implementation.

Execution strategy (important):
- This initialization step is only phase 1. Do NOT try to perfect everything in one shot.
- Deliver a runnable minimum implementation first (RESP2 protocol parser + minimal command set + start script), and leave advanced capabilities for later improvement iterations.
- When a requirement is not fully complete yet, implement the best practical subset now and structure code for incremental extension.

Requirements:
1. Use Python and do not depend on any existing Redis server libraries (e.g., no redis-server, no KeyDB). You may use the standard library and common packages.

2. **RESP2 Protocol requirements**:
   - Implement the RESP2 (REdis Serialization Protocol v2) wire protocol
   - **Inline commands**: single-line commands terminated by `\\r\\n` (e.g., `PING\\r\\n`)
   - **Bulk string format**: `$<length>\\r\\n<data>\\r\\n` (including `$-1\\r\\n` for null bulk string)
   - **Array format**: `*<count>\\r\\n` followed by count elements
   - **Simple string response**: `+<string>\\r\\n` (e.g., `+OK\\r\\n`, `+PONG\\r\\n`)
   - **Error response**: `-ERR <message>\\r\\n` or `-WRONGTYPE <message>\\r\\n`
   - **Integer response**: `:<number>\\r\\n`
   - Must handle partial reads and multi-bulk requests correctly
   - RESP3 is NOT required

3. **Required minimum commands** (implement at minimum):
   - `PING` — return `+PONG\\r\\n`
   - `ECHO <message>` — return the message as bulk string
   - `SET key value [EX seconds] [PX milliseconds] [NX|XX]` — store a key-value pair
   - `GET key` — retrieve value by key
   - `DEL key [key ...]` — delete one or more keys, return count of deleted keys
   - `EXISTS key [key ...]` — return count of existing keys
   - `COMMAND` — return a valid response (can be minimal/empty array)
   - `QUIT` — close connection gracefully

4. **Data type roadmap** (do NOT implement all now, but structure code for these):
   - Stage A: Strings + key expiry (SET/GET/DEL/EXISTS/EXPIRE/TTL/PTTL/PERSIST/INCR/DECR/INCRBY/DECRBY/APPEND/STRLEN/MGET/MSET/SETNX/SETEX/PSETEX/GETSET/INCRBYFLOAT)
   - Stage B: Lists (LPUSH/RPUSH/LPOP/RPOP/LLEN/LRANGE/LINDEX/LSET/LINSERT/LREM/RPOPLPUSH)
   - Stage C: Hashes (HSET/HGET/HDEL/HEXISTS/HGETALL/HMSET/HMGET/HINCRBY/HINCRBYFLOAT/HKEYS/HVALS/HLEN/HSETNX)
   - Stage D: Sets (SADD/SREM/SMEMBERS/SISMEMBER/SCARD/SUNION/SINTER/SDIFF/SPOP/SRANDMEMBER/SMOVE/SUNIONSTORE/SINTERSTORE/SDIFFSTORE)
   - Stage E: Sorted Sets (ZADD/ZREM/ZSCORE/ZRANK/ZREVRANK/ZRANGE/ZREVRANGE/ZRANGEBYSCORE/ZREVRANGEBYSCORE/ZCARD/ZCOUNT/ZINCRBY/ZPOPMIN/ZPOPMAX/ZUNIONSTORE/ZINTERSTORE)
   - Stage F: Persistence (RDB snapshots, AOF append-only file, BGSAVE/BGREWRITEAOF/SAVE)
   - Stage G: Pub/Sub (SUBSCRIBE/UNSUBSCRIBE/PUBLISH/PSUBSCRIBE/PUNSUBSCRIBE)
   - Stage H: Transactions (MULTI/EXEC/DISCARD/WATCH/UNWATCH) and pipelining
   - Stage I: SCAN/SSCAN/HSCAN/ZSCAN, SELECT (multi-DB), DBSIZE/FLUSHDB/FLUSHALL/KEYS/RANDOMKEY/RENAME/RENAMENX/TYPE/OBJECT
   - Stage J: INFO, CONFIG GET/SET (subset), CLIENT LIST/SETNAME/GETNAME, DEBUG (subset)

5. **Architecture requirements**:
   - Must support concurrent connections (multi-threading or asyncio)
   - Implement proper RESP2 frame parsing and serialization
   - Handle pipelined commands (multiple commands sent before reading responses)
   - Support at least 16 logical databases (SELECT 0-15)

6. **Robustness requirements**:
   - Handle `SIGTERM` and `SIGINT` for graceful shutdown and proper socket/port release
   - Implement solid exception handling so a single connection error does not crash the whole server
   - Handle partial reads, malformed commands, and connection resets gracefully

7. **[CRITICAL] Create a startup script `start.sh`** and read host/port from environment variables `REDIS_HOST`/`REDIS_PORT`. Default port: 6379.
   - **This is the MOST IMPORTANT deliverable. Without a working `start.sh`, the system CANNOT be tested at all and all benchmarks will fail.**
   - `start.sh` must be in the project root directory, must be executable, and must start the server in the foreground (or via nohup).
   - The server process started by `start.sh` must listen on the port specified by `REDIS_PORT`.
   - Do NOT delete, rename, or break `start.sh` under any circumstances.

8. No authentication is required for the first version (no AUTH command needed).

9. **Exclusions** (do NOT implement):
   - RESP3 protocol
   - Replication (SLAVEOF/REPLICAOF)
   - Cluster mode (CLUSTER commands)
   - Lua scripting (EVAL/EVALSHA)
   - ACL / complex authentication
Scope guardrails (important):
- Treat `./spec` as broad Redis reference material, not as a checklist to fully clone upstream Redis.
- Ignore module/enterprise/current-only content even if it appears in docs (for example FT.*, TS.*, ACL, CLUSTER, EVAL, RESP3-only replies, or newer admin fields).
- For `INFO`, `CONFIG GET`, `CLIENT LIST`, and `OBJECT ENCODING`, implement only a small RESP2-compatible subset first; expand later only if broader compatibility requirements emerge.
- Prioritize solid Redis-compatible behavior for common string-value workloads before expanding feature breadth.
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
      - id: unique identifier (e.g., P1-RESP-001)
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
        Get the improvement prompt for enhancing the Redis-compatible KV store.

        Args:
            iteration: Current improvement iteration number
            feedback: Optional feedback from previous benchmarks

        Returns:
            Improvement prompt string
        """
        if feedback is None:
            feedback = self.read_feedback()

        spec_guidance = self._build_spec_guidance(5)

        prompt = f"""Improve the Redis-compatible KV store implementation in the current directory.

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

**[CRITICAL] `start.sh` is the entry point used by the test runner to start the server. Without a working `start.sh` in the project root, NO benchmarks can run and ALL tests will fail. Never delete, rename, or break `start.sh`. After every change, verify that `bash start.sh` still starts the server correctly on the port specified by `REDIS_PORT`.**

This is improvement iteration #{iteration}. Please:
1. Analyze the current codebase and identify improvement opportunities.
2. Improve RESP2 protocol compliance, command coverage, or stability.
3. Target progressive capability: strings → lists/hashes/sets/sorted sets → persistence → transactions → SCAN.
4. Design and write comprehensive test cases, run them, and fix code defects based on observed results.
   - RESP2 protocol parsing test (inline and bulk string formats)
   - SET/GET/DEL roundtrip test
   - Data structure operation test (lists, hashes, sets, sorted sets)
   - Concurrent connection test
   - Pipelining test (multiple commands without waiting for response)
Scope guardrails (important):
- Keep implementation scope aligned with the local benchmark target, not the full upstream Redis docs.
- Do not chase RESP3, ACL/AUTH, CLUSTER, EVAL/EVALSHA, module commands, or other unsupported features unless current local tests explicitly require them.
- When docs describe multiple versions or richer admin outputs, implement the smallest subset needed by local tests for `INFO`, `CONFIG GET`, `CLIENT LIST`, and `OBJECT ENCODING`.
- Treat workload compatibility as string-value mode plus protocol correctness and successful command completion; do not expand scope just because a doc page mentions extra features.
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
        Find the Redis KV store start script.

        Returns:
            Path to start script or None
        """
        possible_names = [
            "start.sh",
            "start.py",
            "redis_server.py",
            "server.py",
            "kvstore.py",
            "main.py",
        ]

        for name in possible_names:
            script = self.work_dir / name
            if script.exists():
                return script

        py_files = list(self.work_dir.glob("*.py"))
        for f in py_files:
            if "server" in f.name.lower() or "redis" in f.name.lower():
                return f

        if py_files:
            return py_files[0]

        return None

    def _try_resp_ping(self, host: str, port: int) -> bool:
        """Try a RESP2 PING command to verify the server responds."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((host, port))
            # Send inline PING
            sock.sendall(b"PING\r\n")
            response = sock.recv(256)
            sock.close()
            # Accept +PONG or any valid RESP response
            return response.startswith(b"+PONG") or response.startswith(b"+") or response.startswith(b"$")
        except Exception:
            return False


# Register the SUT
from ..registry import register_sut
register_sut("redis_kvstore", RedisKVStoreSUT)
