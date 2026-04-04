"""
Database System Under Test Implementation

MySQL-like database implementation that can be generated and improved by AI agents.
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


class DatabaseSUT(SystemUnderTest):
    """
    MySQL-like Database System Under Test.

    This SUT type generates a MySQL-compatible database server that:
    - Implements MySQL wire protocol
    - Supports basic SQL commands (CREATE, INSERT, SELECT, UPDATE, DELETE)
    - Provides concurrent connection handling
    - Includes transaction support

    Evaluated via external SQL benchmarks covering OLTP and OLAP workloads.
    """

    name = "database"
    description = "MySQL-compatible database server"
    default_port = 3306

    # Default database credentials (configurable via environment)
    DEFAULT_USER = os.environ.get("DB_DEFAULT_USER", "root")
    DEFAULT_PASSWORD = os.environ.get("DB_DEFAULT_PASSWORD", "root")

    def __init__(
        self,
        work_dir: Path,
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(work_dir, config)
        self.user = self.config.get("user", self.DEFAULT_USER)
        self.password = self.config.get("password", self.DEFAULT_PASSWORD)

    def start(
        self,
        host: str = "127.0.0.1",
        port: Optional[int] = None,
        **kwargs
    ) -> Optional[SUTProcess]:
        """
        Start the database server.

        Args:
            host: Host address to bind to
            port: Port to listen on (default: 3306 or from config)
            **kwargs: Additional arguments (log_file, etc.)

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

            logger.info(f"Starting database: {' '.join(cmd)}")
            env = {**os.environ, "DB_HOST": host, "DB_PORT": str(port)}

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
                success, nohup_pid = self._detect_nohup_process(host, port, log_file)
                if success:
                    sut_process.nohup_pid = nohup_pid
                    self._process = sut_process
                    return sut_process
                else:
                    logger.error("Database failed to start (nohup mode)")
                    sut_process.close_log_handle()
                    return None
            else:
                # Normal process - check if still running
                if proc.poll() is not None:
                    logger.error(f"Database process exited immediately with code: {proc.returncode}")
                    sut_process.close_log_handle()
                    if log_file.exists():
                        content = log_file.read_text()[:1000]
                        logger.error(f"Log content:\n{content}")
                    return None

                logger.info(f"Database started, PID: {proc.pid}")
                self._process = sut_process
                return sut_process

        except Exception as e:
            logger.error(f"Failed to start database: {e}")
            return None

    def check_ready(
        self,
        host: str,
        port: int,
        timeout: int = 30,
        **kwargs
    ) -> bool:
        """
        Check if database is ready to accept connections.

        Args:
            host: Host address
            port: Port number
            timeout: Maximum seconds to wait
            **kwargs: user, password for connection test

        Returns:
            True if database is ready
        """
        user = kwargs.get("user", self.user)
        password = kwargs.get("password", self.password)

        logger.info(f"Waiting for database to be ready (max {timeout}s)...")
        self.last_ready_error = None
        last_conn_error: Optional[str] = None

        # Try to import pymysql for actual connection test
        try:
            import pymysql
            has_pymysql = True
        except ImportError:
            logger.warning("pymysql not installed, using port check only")
            has_pymysql = False

        port_was_open = False

        for i in range(timeout):
            try:
                # First check if port is open
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    port_was_open = True
                    # Port is open
                    if has_pymysql:
                        try:
                            conn = pymysql.connect(
                                host=host,
                                port=port,
                                user=user,
                                password=password,
                                connect_timeout=2
                            )
                            conn.close()
                            logger.info("Database is ready (port and connection OK)")
                            return True
                        except Exception as e:
                            last_conn_error = str(e)
                            logger.info(f"Port open but connection failed: {e}")
                    else:
                        logger.info("Database port is open")
                        return True
            except Exception as e:
                logger.debug(f"Port check error: {e}")

            time.sleep(1)
            if (i + 1) % 5 == 0:
                logger.info(f"Still waiting... ({i + 1}/{timeout})")

        if port_was_open and last_conn_error:
            self.last_ready_error = (
                f"Port {port} is open but MySQL protocol connection failed: "
                f"{last_conn_error}"
            )
        elif not port_was_open:
            self.last_ready_error = f"Port {port} never became reachable"

        logger.warning(
            "Database did not become ready in time%s",
            f" ({self.last_ready_error})" if self.last_ready_error else "",
        )
        return False

    def stop(self) -> bool:
        """
        Stop the running database server.

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
            logger.warning("Database still listening on %s:%s after stop; trying fallback cleanup", host, port)

            # 1) Kill lingering local listener process by port.
            self._kill_listener_on_port(host, port)

            # 2) If still occupied, cleanup docker containers publishing this port.
            if self._check_port_in_use(host, port):
                if self._cleanup_docker_by_port(port):
                    self._wait_for_port_release(host, port, timeout=10.0)

            if self._check_port_in_use(host, port):
                logger.error("Database cleanup incomplete: %s:%s is still in use", host, port)
                result = False

        self._process = None
        return result

    def _find_spec_files(self) -> list:
        """Find spec files under work_dir/spec (supports .md and .txt)."""
        spec_files: list = []
        spec_database_dir = self.work_dir / "spec" / "database"
        if spec_database_dir.is_dir():
            spec_files = sorted(
                str(p.relative_to(self.work_dir)).replace("\\", "/")
                for p in spec_database_dir.rglob("*")
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
        Get the initialization prompt for creating a MySQL-like database.

        Returns:
            Initialization prompt string
        """
        spec_guidance = self._build_spec_guidance(11)

        return f"""Build a custom MySQL-like database implementation.

Execution strategy (important):
- This initialization step is only phase 1. Do NOT try to perfect everything in one shot.
- Deliver a runnable minimum implementation first (core protocol + basic SQL path + start script), and write test cases with pymysql and mysql client, run and fix bugs based on observed results. Leave advanced capabilities for later improvement iterations.
- When a requirement is not fully complete yet, implement the best practical subset now and structure code for incremental extension.

Requirements:
1. Use Python and do not depend on existing database libraries.
2. Implement core MySQL protocol behavior, including Handshake V10, authentication (`mysql_native_password`), at least COM_QUERY + OK/ERR/basic ResultSet, and COM_INIT_DB/COM_PING/COM_QUIT, and must accept external MySQL clients over TCP host/port,. Common version/variable probe queries may return fixed values/no-op but must not fail.
3. **Architecture requirements**:
   - Must support **concurrent connections** (multi-threading or asyncio).
   - Implement basic **concurrency control** (for example, read-write locks) to avoid data races under concurrent writes.
   - The storage engine must be designed for persistence (for example, WAL + in-memory indexes), not just an in-memory dictionary.
   - Include a system catalog/metadata layer (`information_schema`) for databases, tables, columns, indexes, constraints, engines, etc., with persistent recovery support.
4. Implement core SQL commands: CREATE DATABASE, CREATE TABLE, SHOW, INSERT, SELECT, UPDATE, DELETE.
5. **Robustness requirements**:
   - Handle `SIGTERM` and `SIGINT` for graceful shutdown and proper socket/port release.
   - Implement solid exception handling so a single connection error does not crash the whole server.
6. **Compatibility requirements (for standard OLTP/OLAP benchmark workloads)**:
   - Must support transactions and connection-level autocommit: BEGIN/COMMIT/ROLLBACK, SET autocommit=0/1.
   - DDL must support PRIMARY KEY, INDEX/KEY, NOT NULL, DEFAULT, AUTO_INCREMENT. FOREIGN KEY may be syntax-compatible without strict enforcement.
   - Must provide schema introspection: `information_schema` (SCHEMATA/TABLES/COLUMNS) + SHOW TABLES/COLUMNS/INDEX/CREATE TABLE, generated dynamically from the persisted catalog.
   - In addition to COM_QUERY, protocol layer must support COM_INIT_DB/COM_PING/COM_QUIT, and prepared statements (COM_STMT_PREPARE/EXECUTE/CLOSE) with `?` binding are recommended.
   - Query engine should support complex SQL: multi-table JOIN, GROUP BY/HAVING, ORDER BY/LIMIT, aggregates, DISTINCT, BETWEEN/IN/LIKE/IS NULL, and common date/string functions (YEAR/EXTRACT, SUBSTRING, COALESCE, CASE).
   - Support multi-row INSERT; optionally support LOAD DATA LOCAL INFILE.
7. **[CRITICAL] Create a startup script `start.sh`** and read the port from environment variable `DB_PORT`.
   - **This is the MOST IMPORTANT deliverable. Without a working `start.sh`, the system CANNOT be tested at all and all benchmarks will fail.**
   - `start.sh` must be in the project root directory, must be executable, and must start the server in the foreground (or via nohup).
   - The server process started by `start.sh` must listen on the port specified by `DB_PORT`.
   - Do NOT delete, rename, or break `start.sh` under any circumstances.
8. Default user: {self.user}, password: {self.password}.
9. Design and write comprehensive test cases with pymysql and mysql client for protocol correctness and SQL execution, run and fix bugs based on observed results.
10. **Future progression** (do NOT implement now, but structure code for these):
   - Stage A: core MySQL protocol correctness and basic SQL engine (single-table CRUD)
   - Stage B: multi-table DDL/DML compatibility and schema introspection (information_schema, SHOW commands)
   - Stage C: transaction support (BEGIN/COMMIT/ROLLBACK) and concurrent connection handling
   - Stage D: complex SQL (JOINs, GROUP BY, aggregates, subqueries) and transactional workloads
   - Stage E: analytical query support, performance optimization, and persistence durability
{spec_guidance}
12. PLAN.md requirements :
    Create a structured PLAN.md to guide future iterations. PLAN.md must must follow a structured state-machine format.
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
      - acceptance_tests: [shell or mysql/pymysql commands]
      - notes: ...
   C. Phase 1 Constraint
      - PLAN.md should define a clear roadmap for later iterations.
      - Keep total tasks under 200 items.
      - Only one task should be marked IN_PROGRESS at initialization.
      - All Phase 1 deliverables must have concrete acceptance_tests.
13.{self.get_git_init_guidance()}

Please deliver Phase 1: a runnable minimal implementation + clear plan in PLAN.md for later iterations."""

    def get_improve_prompt(self, iteration: int, feedback: Optional[str] = None) -> str:
        """
        Get the improvement prompt for enhancing the database.

        Args:
            iteration: Current improvement iteration number
            feedback: Optional feedback from previous benchmarks

        Returns:
            Improvement prompt string
        """
        if feedback is None:
            feedback = self.read_feedback()

        spec_guidance = self._build_spec_guidance(5)

        prompt = f"""Improve the MySQL-like database implementation in the current directory.
        
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

**[CRITICAL] `start.sh` is the entry point used by the test runner to start the server. Without a working `start.sh` in the project root, NO benchmarks can run and ALL tests will fail. Never delete, rename, or break `start.sh`. After every change, verify that `bash start.sh` still starts the server correctly on the port specified by `DB_PORT`.**

This is improvement iteration #{iteration}. Please:
1. Analyze the current codebase and identify improvement opportunities.
2. Improve performance, functionality, or stability.
3. Design and write comprehensive test cases with pymysql and mysql client, run them, and fix code defects based on observed results.
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
        Find the database start script.

        Returns:
            Path to start script or None
        """
        # Database-specific script names
        possible_names = [
            "start.sh",
            "start.py",
            "mysql_server.py",
            "server.py",
            "main.py",
        ]

        for name in possible_names:
            script = self.work_dir / name
            if script.exists():
                return script

        # Look for Python files with server-related names
        py_files = list(self.work_dir.glob("*.py"))
        for f in py_files:
            if "server" in f.name.lower() or "mysql" in f.name.lower():
                return f

        # Return first Python file if any
        if py_files:
            return py_files[0]

        return None

    def get_connection_config(self) -> Dict[str, Any]:
        """Get database connection configuration."""
        config = self.get_connection_info()
        config.update({
            "user": self.user,
            "password": self.password,
        })
        return config


# Register the SUT
from ..registry import register_sut
register_sut("database", DatabaseSUT)
