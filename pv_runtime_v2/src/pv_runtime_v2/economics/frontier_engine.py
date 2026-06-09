from pv_runtime_v2.economics.frontier_policy import (
    FrontierPolicy,
)

from pv_runtime_v2.economics.swarm_optimizer import (
    SwarmOptimizer,
)


class FrontierEngine:

    def __init__(self):

        self.optimizer = (
            SwarmOptimizer()
        )

    def evaluate(
        self,
        policy: FrontierPolicy,
    ):

        agents, utility = (
            self.optimizer.optimal_size(
                trust=policy.trust,
                impact=policy.impact,
                latency_per_agent=policy.latency_ms,
                failure_risk=policy.failure_risk,
                max_agents=policy.max_agents,
            )
        )

        return {
            "optimal_agents": agents,
            "utility": utility,
        }
