from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ClusterState:

    cluster_id: str

    members: int

    approval_ratio: float

    confidence: float
