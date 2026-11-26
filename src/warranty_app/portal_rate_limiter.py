import math
import threading
import time
from collections import deque
from typing import Callable, Dict, Optional


class PortalRateLimiter:
    """A bounded, thread-safe sliding window for the single-process demo app.

    Only the client address and timestamps are retained, never lookup codes.
    A shared limiter (for example Redis) is needed when running multiple workers.
    """

    def __init__(
        self,
        max_attempts: int = 5,
        window_seconds: int = 60,
        clock: Callable[[], float] = time.monotonic,
        max_clients: int = 10000,
    ) -> None:
        if max_attempts < 1 or window_seconds < 1 or max_clients < 1:
            raise ValueError("Rate limiter settings must be positive.")
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._clock = clock
        self._max_clients = max_clients
        self._attempts: Dict[str, deque] = {}
        self._lock = threading.Lock()

    def consume(self, client_address: str) -> Optional[int]:
        """Record a request, or return the number of seconds until retry."""
        with self._lock:
            now = self._clock()
            cutoff = now - self.window_seconds
            expired = []
            for key, attempts in self._attempts.items():
                while attempts and attempts[0] <= cutoff:
                    attempts.popleft()
                if not attempts:
                    expired.append(key)
            for key in expired:
                del self._attempts[key]

            attempts = self._attempts.get(client_address)
            if attempts is None:
                if len(self._attempts) >= self._max_clients:
                    return self.window_seconds
                attempts = deque()
                self._attempts[client_address] = attempts

            if len(attempts) >= self.max_attempts:
                return max(1, math.ceil(attempts[0] + self.window_seconds - now))
            attempts.append(now)
            return None
