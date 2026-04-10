class IdempotencyStore:

    def __init__(self):
        self.memory_store = {}

    def reset(self):
        self.memory_store = {}

    def check_or_store(self, agent_id, action, result=None):
        key = action.get("idempotency_key")

        if not key:
            return {"duplicate": False, "key": None}

        if key in self.memory_store:
            return {"duplicate": True, "result": self.memory_store[key]}

        if result:
            self.memory_store[key] = result

        return {"duplicate": False, "key": key}
