class MeshDecisionEngine:

    def __init__(self, quorum):
        self.quorum = quorum

    def evaluate(self, action_id):
        if self.quorum.check_quorum(action_id):
            return {"decision": "APPROVE"}
        return {"decision": "REJECT"}
