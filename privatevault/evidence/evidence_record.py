import hashlib
import json
import time


class EvidenceRecord:
    """
    Immutable record of an AI action.
    """

    def __init__(self, action, result):
        self.timestamp = time.time()
        self.agent_id = action.agent_id
        self.intent = action.intent
        self.tool = action.tool
        self.parameters = action.parameters
        self.result = result

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "agent_id": self.agent_id,
            "intent": self.intent,
            "tool": self.tool,
            "parameters": self.parameters,
            "result": self.result
        }

    def hash(self):
        payload = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()
