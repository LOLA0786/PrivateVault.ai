class TrustEngine:

    def evaluate(self, outcome):

        if outcome.get("success"):
            return 95

        return 50
