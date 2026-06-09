from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class LeaderState:

    cluster_id: str

    healthy: bool

    trust_score: float
