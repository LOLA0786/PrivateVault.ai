from typing import Iterable

from pv_runtime_v2.consensus.cluster_quorum import (
    ClusterVote,
)


class GlobalQuorum:

    THRESHOLD = 0.67

    def approved(
        self,
        votes: Iterable[
            ClusterVote
        ],
    ) -> bool:

        votes = list(votes)

        if not votes:
            return False

        score = (
            sum(
                v.approval_ratio
                for v in votes
            )
            / len(votes)
        )

        return (
            score >= self.THRESHOLD
        )
