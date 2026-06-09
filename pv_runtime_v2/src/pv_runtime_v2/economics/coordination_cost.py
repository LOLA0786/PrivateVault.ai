class CoordinationCost:

    def calculate(
        self,
        agents: int,
        latency_ms: float,
    ) -> float:

        return (
            agents * latency_ms
        )
