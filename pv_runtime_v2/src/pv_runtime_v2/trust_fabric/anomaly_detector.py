class AnomalyDetector:

    TRUST_THRESHOLD = 0.50

    def compromised(
        self,
        trust_score: float,
    ) -> bool:

        return (
            trust_score
            < self.TRUST_THRESHOLD
        )
