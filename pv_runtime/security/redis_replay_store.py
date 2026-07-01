"""
Redis replay store.
"""

import redis

from pv_runtime.security.replay_store import ReplayStore


class RedisReplayStore(ReplayStore):

    def __init__(
        self,
        host="localhost",
        port=6379,
    ):

        self.redis = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
        )

    def exists(self, key):

        return self.redis.exists(key)

    def put(
        self,
        key,
        ttl,
    ):

        self.redis.setex(
            key,
            max(ttl, 1),
            "1",
        )
