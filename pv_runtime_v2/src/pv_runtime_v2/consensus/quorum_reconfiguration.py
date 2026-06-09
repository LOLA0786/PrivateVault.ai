from pv_runtime_v2.consensus.leader_state import (
    LeaderState,
)


class QuorumReconfiguration:

    def replace(
        self,
        failed: LeaderState,
    ) -> LeaderState:

        return LeaderState(
            cluster_id=failed.cluster_id,
            healthy=True,
            trust_score=1.0,
        )
