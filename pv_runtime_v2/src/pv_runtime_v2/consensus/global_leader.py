from typing import Iterable

from pv_runtime_v2.consensus.cluster_state import (
    ClusterState,
)


class GlobalLeader:

    THRESHOLD = 0.67

    def approve(
        self,
        states: Iterable[
            ClusterState
        ],
    ) -> bool:

        states = list(states)

        score = (
            sum(
                s.confidence
                for s in states
            )
            / len(states)
        )

        return (
            score >= self.THRESHOLD
        )
