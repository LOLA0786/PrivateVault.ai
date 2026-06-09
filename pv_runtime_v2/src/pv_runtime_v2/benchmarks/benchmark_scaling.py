import time

from pv_runtime_v2.consensus.weighted_quorum import (
    Vote,
)

from pv_runtime_v2.consensus.cluster_quorum import (
    ClusterQuorum,
)

from pv_runtime_v2.consensus.global_quorum import (
    GlobalQuorum,
)


def benchmark(
    agents: int,
    clusters: int,
    events: int,
):

    cluster_quorum = ClusterQuorum()

    global_quorum = GlobalQuorum()

    agents_per_cluster = (
        agents // clusters
    )

    votes = [
        Vote(
            weight=1.0,
            approve=True,
        )
        for _ in range(
            agents_per_cluster
        )
    ]

    start = (
        time.perf_counter()
    )

    for _ in range(events):

        cluster_votes = []

        for cluster in range(clusters):

            cluster_votes.append(
                cluster_quorum
                .evaluate_cluster(
                    f"c-{cluster}",
                    votes,
                )
            )

        global_quorum.approved(
            cluster_votes
        )

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    print(
        f"{agents=} "
        f"{clusters=} "
        f"{events=} "
        f"{elapsed:.2f} ms"
    )


if __name__ == "__main__":

    benchmark(
        agents=100,
        clusters=10,
        events=10000,
    )

    benchmark(
        agents=1000,
        clusters=20,
        events=10000,
    )

    benchmark(
        agents=10000,
        clusters=50,
        events=10000,
    )
