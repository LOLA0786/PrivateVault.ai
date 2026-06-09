from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ClusterHealth:

    cluster_id: str

    healthy_agents: int

    quarantined_agents: int

    health_score: float
