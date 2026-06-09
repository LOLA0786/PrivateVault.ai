class DecisionValue:

    def calculate(
        self,
        confidence: float,
        impact: float,
    ) -> float:

        return (
            confidence * impact
        )
