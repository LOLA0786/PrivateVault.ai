from pv_runtime_v2.economics.coordination_cost import (
    CoordinationCost,
)

from pv_runtime_v2.economics.decision_value import (
    DecisionValue,
)

from pv_runtime_v2.economics.utility_function import (
    UtilityFunction,
)


class CoordinationOptimizer:

    def __init__(self):

        self.cost = (
            CoordinationCost()
        )

        self.value = (
            DecisionValue()
        )

        self.utility = (
            UtilityFunction()
        )

    def should_expand(
        self,
        current_agents: int,
        expected_confidence_gain: float,
        impact: float,
        latency_ms: float,
    ) -> bool:

        value = (
            self.value.calculate(
                expected_confidence_gain,
                impact,
            )
        )

        cost = (
            self.cost.calculate(
                current_agents,
                latency_ms,
            )
        )

        utility = (
            self.utility.score(
                value,
                cost,
            )
        )

        return utility > 0
