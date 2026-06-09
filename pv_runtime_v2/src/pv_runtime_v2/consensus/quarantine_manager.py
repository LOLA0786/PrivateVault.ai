class QuarantineManager:

    def should_quarantine(
        self,
        trust_score: float,
    ) -> bool:

        return (
            trust_score < 0.50
        )
