from collections import defaultdict

class WeightedQuorum:

    def __init__(self, threshold, trust_registry):
        self.threshold = threshold
        self.votes = defaultdict(list)
        self.trust_registry = trust_registry

    def submit_vote(self, action_id, agent_id, vote, signature):
        self.votes[action_id].append({
            "agent": agent_id,
            "vote": vote,
            "signature": signature
        })

    def check_quorum(self, action_id):
        votes = self.votes[action_id]

        score = 0.0

        for v in votes:
            if v["vote"] == "APPROVE":
                trust = self.trust_registry.get(v["agent"], 0.5)
                score += trust

        return score >= self.threshold
