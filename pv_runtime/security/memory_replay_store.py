"""
In-memory replay store.

Useful for unit tests and local development.
"""

import time

from pv_runtime.security.replay_store import ReplayStore


class MemoryReplayStore(ReplayStore):

    def __init__(self):
        self._cache = {}

    def exists(self, key):

        now = time.time()

        expired = [
            k
            for k, v in self._cache.items()
            if v <= now
        ]

        for k in expired:
            del self._cache[k]

        return key in self._cache

    def put(self, key, ttl):

        self._cache[key] = time.time() + ttl
