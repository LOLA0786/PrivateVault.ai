class SuccessEngine:

    def evaluate(self, outcome):

        if outcome.get("success"):
            return 100

        return 0
