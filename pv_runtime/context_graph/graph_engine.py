from pv_runtime.context_graph.persistence.redis_graph import RedisGraph
redis_graph = RedisGraph()

from typing import Dict, Any
import uuid
import time

class ContextGraph:
    def reset(self):
        self.nodes = {}
        self.edges = []


    def __init__(self):
        self.nodes = {}
        self.edges = []

    def record_intent(self, agent_id: str, action: Dict[str, Any]):
        redis_graph.record_node("intent", agent_id, action)

        node_id = str(uuid.uuid4())

        self.nodes[node_id] = {
            "type": "intent",
            "agent": agent_id,
            "action": action,
            "timestamp": time.time()
        }

    def record_outcome(self, agent_id: str, action: Dict, result: Dict):
        redis_graph.record_node("outcome", agent_id, result)

        node_id = str(uuid.uuid4())

        self.nodes[node_id] = {
            "type": "outcome",
            "agent": agent_id,
            "action": action,
            "result": result,
            "timestamp": time.time()
        }

    def query(self, agent_id: str):
        return [n for n in self.nodes.values() if n["agent"] == agent_id]
