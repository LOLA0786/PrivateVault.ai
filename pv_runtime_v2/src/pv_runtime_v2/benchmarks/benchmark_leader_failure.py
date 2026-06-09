from pv_runtime_v2.consensus.leader_state import (
    LeaderState,
)

from pv_runtime_v2.consensus.byzantine_quorum import (
    ByzantineQuorum,
)

from pv_runtime_v2.consensus.quorum_reconfiguration import (
    QuorumReconfiguration,
)


def scenario(
    failed_leaders: int,
):

    leaders = []

    for i in range(50):

        leaders.append(
            LeaderState(
                cluster_id=f"c-{i}",
                healthy=True,
                trust_score=1.0,
            )
        )

    for i in range(
        failed_leaders
    ):

        leaders[i] = (
            LeaderState(
                cluster_id=f"c-{i}",
                healthy=False,
                trust_score=0.0,
            )
        )

    quorum = (
        ByzantineQuorum()
    )

    before = (
        quorum.available(
            leaders
        )
    )

    reconf = (
        QuorumReconfiguration()
    )

    repaired = []

    for leader in leaders:

        if not leader.healthy:

            repaired.append(
                reconf.replace(
                    leader
                )
            )

        else:

            repaired.append(
                leader
            )

    after = (
        quorum.available(
            repaired
        )
    )

    print(
        f"failed={failed_leaders} "
        f"before={before} "
        f"after={after}"
    )


if __name__ == "__main__":

    scenario(5)

    scenario(10)

    scenario(15)

    scenario(20)

    scenario(25)

    scenario(30)
