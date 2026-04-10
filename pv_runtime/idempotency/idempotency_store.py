import json
import hashlib

class IdempotencyStore:
    def reset(self):
        if self.redis_enabled:
            self.r.flushdb()
        else:
            self.memory_store = {}


    def __init__(self):
        self.memory_store = {}
        self.redis_enabled = False

        try:
            import redis
            self.r = redis.Redis(host="localhost", port=6379, decode_responses=True)
            self.r.ping()
            self.redis_enabled = True
        except Exception:
            self.redis_enabled = False

    def _hash(self, agent_id, action):
        raw = f"{agent_id}:{json.dumps(action, sort_keys=True)}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def check_or_store(self, agent_id, action, result=None):
        key = self._hash(agent_id, action)

        # --- REDIS MODE ---
        if self.redis_enabled:
            existing = self.r.get(key)
            if existing:
                return {"duplicate": True, "result": json.loads(existing)}

            if result:
                self.r.set(key, json.dumps(result))

            return {"duplicate": False, "key": key}

        # --- FALLBACK MEMORY MODE ---
        if key in self.memory_store:
            return {"duplicate": True, "result": self.memory_store[key]}

        if result:
            self.memory_store[key] = result

        return {"duplicate": False, "key": key}
