import time

class LockManager:

    def __init__(self):
        self.memory_locks = {}

    def acquire_lock(self, key, ttl=5):
        now = time.time()

        if key in self.memory_locks:
            if now < self.memory_locks[key]:
                return False

        self.memory_locks[key] = now + ttl
        return True

    def release_lock(self, key):
        if key in self.memory_locks:
            del self.memory_locks[key]

    def execute_with_lock(self, key, func):
        if not self.acquire_lock(key):
            return {"status": "LOCKED"}

        try:
            return func()
        finally:
            self.release_lock(key)
