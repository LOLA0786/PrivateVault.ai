from pv_runtime_v2.consensus.cluster_health import (
    ClusterHealth,
)


class HealthCalculator:

    def evaluate(
        self,
        cluster_id: str,
        healthy_agents: int,
        quarantined_agents: int,
    ) -> ClusterHealth:

        total = (
            healthy_agents
            + quarantined_agents
        )

        if total == 0:
            score = 0.0
        else:
            score = (
                healthy_agents
                / total
            )

        return ClusterHealth(
            cluster_id=cluster_id,
            healthy_agents=healthy_agents,
            quarantined_agents=quarantined_agents,
            health_score=score,
        )
