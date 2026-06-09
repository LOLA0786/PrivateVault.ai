import time

from pv_runtime_v2.consensus.cluster_leader import (
    ClusterLeader,
)

from pv_runtime_v2.consensus.global_leader import (
    GlobalLeader,
)


def run():

    leader = ClusterLeader()

    global_leader = GlobalLeader()

    states = []

    for cluster in range(50):

        states.append(
            leader.summarize(
                cluster_id=f"c-{cluster}",
                members=200,
                approval_ratio=0.95,
            )
        )

    start = time.perf_counter()

    for _ in range(100000):

        global_leader.approve(
            states
        )

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    print(
        f"100000 decisions "
        f"{elapsed:.2f} ms"
    )


if __name__ == "__main__":
    run()
