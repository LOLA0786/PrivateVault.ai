class ConsensusEngine:

    def evaluate(
        self,
        trust_score: float
    ) -> float:

        if trust_score >= 0.90:
            return 1.0

        if trust_score >= 0.75:
            return 0.8

        return 0.0
