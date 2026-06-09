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


def build_votes():

    return [
        Vote(
            weight=1.0,
            approve=True,
        )
        for _ in range(10)
    ]


def run():

    cluster_quorum = (
        ClusterQuorum()
    )

    global_quorum = (
        GlobalQuorum()
    )

    start = (
        time.perf_counter()
    )

    for _ in range(10000):

        cluster_votes = []

        for cluster in range(10):

            result = (
                cluster_quorum
                .evaluate_cluster(
                    f"cluster-{cluster}",
                    build_votes(),
                )
            )

            cluster_votes.append(
                result
            )

        global_quorum.approved(
            cluster_votes
        )

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    print(
        f"100 agents "
        f"10000 events "
        f"{elapsed:.2f} ms"
    )


if __name__ == "__main__":
    run()
