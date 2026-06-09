class EconomicsEngine:

    def evaluate(
        self,
        trust_score: float,
        consensus_score: float
    ) -> float:

        return (
            trust_score *
            consensus_score
        )
