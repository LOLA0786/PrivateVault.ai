from dataclasses import dataclass
from typing import Iterable

from pv_runtime_v2.consensus.weighted_quorum import (
    Vote,
    WeightedQuorum,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ClusterVote:

    cluster_id: str

    approval_ratio: float


class ClusterQuorum:

    def __init__(self):

        self.quorum = (
            WeightedQuorum()
        )

    def evaluate_cluster(
        self,
        cluster_id: str,
        votes: Iterable[Vote],
    ) -> ClusterVote:

        ratio = (
            self.quorum.evaluate(
                votes
            )
        )

        return ClusterVote(
            cluster_id=cluster_id,
            approval_ratio=ratio,
        )
