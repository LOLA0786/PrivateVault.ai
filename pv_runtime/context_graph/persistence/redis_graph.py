class RedisGraph:

    def __init__(self):
        self.memory = []

        try:
            import redis
            self.r = redis.Redis(host="localhost", port=6379, decode_responses=True)
            self.r.ping()
            self.redis_enabled = True
        except Exception:
            self.redis_enabled = False

    def record_node(self, node_type, agent_id, payload):
        node = {
            "type": node_type,
            "agent": agent_id,
            "payload": payload
        }

        if self.redis_enabled:
            import json, uuid
            node_id = str(uuid.uuid4())
            self.r.set(f"pv:node:{node_id}", json.dumps(node))
        else:
            self.memory.append(node)

    def get_all(self):
        return self.memory
