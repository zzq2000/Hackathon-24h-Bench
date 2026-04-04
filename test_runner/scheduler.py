"""
Test Scheduler Module

Provides scheduling logic for periodic test execution.
"""

import logging
import signal
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Callable, List

from .core import TestOrchestrator, TestCycleResult

logger = logging.getLogger(__name__)


class TestScheduler:
    """
    Scheduler for periodic test execution.

    Handles:
    - Periodic test cycle execution
    - Graceful shutdown on signals
    - Test result callbacks
    """
    __test__ = False

    def __init__(
        self,
        orchestrator: TestOrchestrator,
        interval_sec: int = 1800,
        benchmark_timeout_sec: int = 600,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize scheduler.

        Args:
            orchestrator: Test orchestrator instance
            interval_sec: Interval between tests in seconds
            benchmark_timeout_sec: Timeout for each benchmark
            config: Additional configuration
        """
        self.orchestrator = orchestrator
        self.interval_sec = interval_sec
        self.benchmark_timeout_sec = benchmark_timeout_sec
        self.config = config or {}

        # State
        self._stop_event = threading.Event()
        self._test_threads: List[threading.Thread] = []
        self._test_index = 0
        self._run_id: Optional[str] = None

        # Callbacks
        self._on_cycle_complete: Optional[Callable[[TestCycleResult], None]] = None
        self._on_cycle_start: Optional[Callable[[str, int], None]] = None

    def set_callbacks(
        self,
        on_cycle_complete: Optional[Callable[[TestCycleResult], None]] = None,
        on_cycle_start: Optional[Callable[[str, int], None]] = None,
    ) -> None:
        """Set callback functions."""
        self._on_cycle_complete = on_cycle_complete
        self._on_cycle_start = on_cycle_start

    def run_once(self, run_id: str) -> TestCycleResult:
        """
        Run a single test cycle.

        Args:
            run_id: Run identifier

        Returns:
            TestCycleResult
        """
        self._run_id = run_id
        self._test_index += 1
        snapshot_time = datetime.now().isoformat(timespec="seconds")

        if self._on_cycle_start:
            self._on_cycle_start(run_id, self._test_index)

        result = self.orchestrator.run_cycle(
            run_id=run_id,
            test_index=self._test_index,
            benchmark_timeout_sec=self.benchmark_timeout_sec,
            snapshot_time=snapshot_time,
        )

        if self._on_cycle_complete:
            self._on_cycle_complete(result)

        return result

    def run_periodic(
        self,
        run_id: str,
        first_delay_sec: Optional[int] = None,
    ) -> None:
        """
        Run periodic test cycles.

        Args:
            run_id: Run identifier
            first_delay_sec: Delay before first test (None = run immediately)
        """
        self._run_id = run_id
        self._stop_event.clear()

        # Setup signal handlers
        original_sigint = signal.signal(signal.SIGINT, self._signal_handler)
        original_sigterm = signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # Wait for first test
            if first_delay_sec and first_delay_sec > 0:
                logger.info(f"Waiting {first_delay_sec}s before first test...")
                next_run = time.time() + first_delay_sec
            else:
                next_run = time.time()

            while not self._stop_event.is_set():
                now = time.time()
                if now >= next_run:
                    # Check if SUT has implementation
                    if self.orchestrator.sut.has_implementation_files():
                        self._submit_test()
                    else:
                        logger.warning("No implementation files, skipping test")

                    next_run = time.time() + self.interval_sec
                    logger.info(f"Next test in {self.interval_sec}s")

                time.sleep(1)

        finally:
            # Restore signal handlers
            signal.signal(signal.SIGINT, original_sigint)
            signal.signal(signal.SIGTERM, original_sigterm)

            # Cleanup
            self.stop()

    def _submit_test(self) -> None:
        """Submit a test cycle to run in a thread."""
        self._test_index += 1
        snapshot_time = datetime.now().isoformat(timespec="seconds")

        if self._on_cycle_start:
            self._on_cycle_start(self._run_id, self._test_index)

        thread = threading.Thread(
            target=self._run_test_thread,
            args=(self._run_id, self._test_index, snapshot_time),
            daemon=True,
        )
        thread.start()
        self._test_threads.append(thread)

        logger.info(f"Submitted test: {self._run_id}/test_instance_{self._test_index}")

    def _run_test_thread(
        self,
        run_id: str,
        test_index: int,
        snapshot_time: str
    ) -> None:
        """Run test cycle in a thread."""
        try:
            result = self.orchestrator.run_cycle(
                run_id=run_id,
                test_index=test_index,
                benchmark_timeout_sec=self.benchmark_timeout_sec,
                snapshot_time=snapshot_time,
            )

            if self._on_cycle_complete:
                self._on_cycle_complete(result)

        except Exception as e:
            logger.error(f"Test thread error: {e}", exc_info=True)

    def _signal_handler(self, sig, frame) -> None:
        """Handle interrupt signals."""
        logger.info(f"\nReceived signal {sig}, stopping...")
        self._stop_event.set()

    def stop(self) -> None:
        """Stop the scheduler and cleanup."""
        self._stop_event.set()
        self.orchestrator.cleanup_all()

        # Wait for threads to complete
        for thread in self._test_threads:
            thread.join(timeout=5)

    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return not self._stop_event.is_set()

    def wait_for_files(
        self,
        max_wait_sec: int = 3600,
        check_interval_sec: int = 30
    ) -> bool:
        """
        Wait for SUT implementation files to exist.

        Args:
            max_wait_sec: Maximum wait time
            check_interval_sec: Check interval

        Returns:
            True if files found
        """
        logger.info(f"Waiting for implementation files (max {max_wait_sec}s)...")

        elapsed = 0
        while elapsed < max_wait_sec:
            if self._stop_event.is_set():
                return False

            if self.orchestrator.sut.has_implementation_files():
                logger.info("Implementation files found")
                return True

            time.sleep(check_interval_sec)
            elapsed += check_interval_sec

            if elapsed % 300 == 0:
                logger.info(f"Still waiting... ({elapsed}/{max_wait_sec}s)")

        logger.warning(f"Timeout waiting for implementation files")
        return False
