from collections import defaultdict
from datetime import datetime

class IntentAccumulationGraph:

    def __init__(self):
        self.sessions = defaultdict(list)

    def add_intent(self, session_id, intent):
        self.sessions[session_id].append({
            "timestamp": datetime.utcnow().isoformat(),
            "intent": intent
        })

    def get_history(self, session_id):
        return self.sessions.get(session_id, [])

    def count(self, session_id):
        return len(self.sessions.get(session_id, []))
