class ContextStitchingDetector:

    RISK_TERMS = {
        "step",
        "combine",
        "continue",
        "previous",
        "earlier",
        "next phase"
    }

    def score(self, history):

        score = 0

        for item in history:
            text = str(item).lower()

            for term in self.RISK_TERMS:
                if term in text:
                    score += 10

        return min(score, 100)
