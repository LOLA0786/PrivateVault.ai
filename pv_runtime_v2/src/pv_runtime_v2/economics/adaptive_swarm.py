from pv_runtime_v2.economics.frontier_policy import (
    FrontierPolicy,
)

from pv_runtime_v2.economics.frontier_engine import (
    FrontierEngine,
)


class AdaptiveSwarm:

    def __init__(self):

        self.engine = (
            FrontierEngine()
        )

    def allocate(
        self,
        trust: float,
        impact: float,
        latency_ms: float,
        failure_risk: float,
    ):

        policy = FrontierPolicy(
            trust=trust,
            impact=impact,
            latency_ms=latency_ms,
            failure_risk=failure_risk,
        )

        return self.engine.evaluate(
            policy
        )
