class DecisionFrontier:

    def utility(
        self,
        confidence: float,
        impact: float,
        latency_ms: float,
        failure_risk: float,
    ) -> float:

        value = (
            confidence * impact
        )

        cost = (
            latency_ms
            + failure_risk
        )

        return (
            value - cost
        )
