from pv_runtime_v2.economics.utility_curve import (
    UtilityCurve,
)

from pv_runtime_v2.economics.decision_frontier import (
    DecisionFrontier,
)


class SwarmOptimizer:

    def __init__(self):

        self.curve = (
            UtilityCurve()
        )

        self.frontier = (
            DecisionFrontier()
        )

    def optimal_size(
        self,
        trust: float,
        impact: float,
        latency_per_agent: float,
        failure_risk: float,
        max_agents: int = 1000,
    ):

        best_agents = 1
        best_utility = float("-inf")

        for agents in range(
            1,
            max_agents + 1,
        ):

            confidence = (
                self.curve.confidence(
                    agents,
                    trust,
                )
            )

            latency = (
                agents
                * latency_per_agent
            )

            utility = (
                self.frontier.utility(
                    confidence,
                    impact,
                    latency,
                    failure_risk,
                )
            )

            if utility > best_utility:

                best_utility = utility
                best_agents = agents

        return (
            best_agents,
            best_utility,
        )
