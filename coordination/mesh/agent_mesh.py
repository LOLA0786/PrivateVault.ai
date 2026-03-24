import hashlib
import json
from datetime import datetime

class AgentMesh:

    def __init__(self):
        self.agents = {}
        self.messages = []

    def register_agent(self, agent_id, public_key, capabilities):
        self.agents[agent_id] = {
            "public_key": public_key,
            "capabilities": capabilities,
            "trust_score": 1.0
        }

    def send_message(self, sender, receiver, payload):
        message = {
            "sender": sender,
            "receiver": receiver,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat()
        }

        message["hash"] = self._hash(message)

        self.messages.append(message)
        return message

    def _hash(self, message):
        return hashlib.sha256(
            json.dumps(message, sort_keys=True).encode()
        ).hexdigest()
