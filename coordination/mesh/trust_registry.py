class TrustRegistry:

    def __init__(self):
        self.scores = {}

    def set_score(self, agent_id, score):
        self.scores[agent_id] = score

    def get(self, agent_id, default=0.5):
        return self.scores.get(agent_id, default)
