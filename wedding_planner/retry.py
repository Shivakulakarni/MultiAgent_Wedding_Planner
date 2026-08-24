from __future__ import annotations

import logging
import time
from typing import Any, Callable

from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

log = logging.getLogger(__name__)

retry_on_api_error = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((ConnectionError, TimeoutError, OSError)),
    reraise=True,
    before_sleep=lambda retry_state: log.warning(
        f"Retry {retry_state.attempt_number}/3 after {retry_state.outcome.exception() if retry_state.outcome else 'unknown'}"
    ),
)


class CircuitBreaker:
    """Circuit breaker: opens after threshold failures, resets after recovery timeout."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failure_count = 0
        self._last_failure_time: float = 0
        self._state = "closed"
        self._lock = __import__("threading").Lock()

    @property
    def state(self) -> str:
        with self._lock:
            if self._state == "open":
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._state = "half-open"
                    log.info("Circuit breaker: half-open (recovery timeout elapsed)")
            return self._state

    def record_success(self) -> None:
        with self._lock:
            self._failure_count = 0
            if self._state != "closed":
                log.info("Circuit breaker: closed (success recorded)")
                self._state = "closed"

    def record_failure(self) -> None:
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._failure_count >= self.failure_threshold:
                self._state = "open"
                log.warning(f"Circuit breaker: OPEN after {self._failure_count} failures")

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Execute func through the circuit breaker. Raises RuntimeError if open."""
        current_state = self.state
        if current_state == "open":
            raise RuntimeError(f"Circuit breaker is OPEN (failures: {self._failure_count})")
        try:
            result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception:
            self.record_failure()
            raise
