from pv_runtime_v2.consensus.cluster_state import (
    ClusterState,
)


class ClusterLeader:

    def summarize(
        self,
        cluster_id: str,
        members: int,
        approval_ratio: float,
    ) -> ClusterState:

        return ClusterState(
            cluster_id=cluster_id,
            members=members,
            approval_ratio=approval_ratio,
            confidence=approval_ratio,
        )
