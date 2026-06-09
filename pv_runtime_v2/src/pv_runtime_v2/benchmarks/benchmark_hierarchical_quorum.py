import time

from pv_runtime_v2.consensus.cluster_leader import (
    ClusterLeader,
)

from pv_runtime_v2.consensus.global_leader import (
    GlobalLeader,
)


def benchmark(
    agents: int,
    clusters: int,
    events: int,
):

    leader = ClusterLeader()

    global_leader = GlobalLeader()

    start = time.perf_counter()

    for _ in range(events):

        states = []

        agents_per_cluster = (
            agents // clusters
        )

        for cluster in range(clusters):

            states.append(
                leader.summarize(
                    cluster_id=f"c-{cluster}",
                    members=agents_per_cluster,
                    approval_ratio=0.95,
                )
            )

        global_leader.approve(
            states
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
