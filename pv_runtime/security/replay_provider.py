"""
Replay provider.

Chooses the replay backend.
"""

import os

from pv_runtime.security.memory_replay_store import MemoryReplayStore
from pv_runtime.security.redis_replay_store import RedisReplayStore


_backend = None


def get_replay_store():

    global _backend

    if _backend is not None:
        return _backend

    backend = os.getenv(
        "PV_REPLAY_BACKEND",
        "memory",
    ).lower()

    if backend == "redis":

        _backend = RedisReplayStore()

    else:

        _backend = MemoryReplayStore()

    return _backend
