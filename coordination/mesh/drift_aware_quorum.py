from collections import defaultdict

# Safe import (do not break if function missing)
try:
    from drift_detection import detect_drift
except:
    def detect_drift(context):
        # fallback logic: treat "drift": True as drift
        if not context:
            return False
        return context.get("drift", False)


class DriftAwareQuorum:

    def __init__(self, threshold, trust_registry):
        self.threshold = threshold
        self.votes = defaultdict(list)
        self.trust_registry = trust_registry

    def submit_vote(self, action_id, agent_id, vote, signature, context=None):
        self.votes[action_id].append({
            "agent": agent_id,
            "vote": vote,
            "signature": signature,
            "context": context
        })

    def check_quorum(self, action_id):
        votes = self.votes[action_id]

        score = 0.0

        for v in votes:

            # 🚨 Drift filter
            if detect_drift(v.get("context")):
                continue

            if v["vote"] == "APPROVE":
                trust = self.trust_registry.get(v["agent"], 0.5)
                score += trust

        return score >= self.threshold
