class ClusterRouter:

    def route(
        self,
        agent_id: str,
        total_clusters: int,
    ) -> int:

        return (
            hash(agent_id)
            % total_clusters
        )
