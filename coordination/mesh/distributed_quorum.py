from collections import defaultdict

class DistributedQuorum:

    def __init__(self, threshold):
        self.threshold = threshold
        self.votes = defaultdict(list)

    def submit_vote(self, action_id, agent_id, vote, signature):
        self.votes[action_id].append({
            "agent": agent_id,
            "vote": vote,
            "signature": signature
        })

    def check_quorum(self, action_id):
        votes = self.votes[action_id]

        approvals = [v for v in votes if v["vote"] == "APPROVE"]

        if len(approvals) >= self.threshold:
            return True

        return False
