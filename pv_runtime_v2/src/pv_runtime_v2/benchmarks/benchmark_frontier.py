from pv_runtime_v2.economics.swarm_optimizer import (
    SwarmOptimizer,
)


def run():

    optimizer = SwarmOptimizer()

    print(
        "trust,impact,optimal_agents"
    )

    trusts = [
        0.3,
        0.5,
        0.7,
        0.9,
    ]

    impacts = [
        100,
        1000,
        10000,
        100000,
    ]

    for trust in trusts:

        for impact in impacts:

            agents, _ = (
                optimizer.optimal_size(
                    trust=trust,
                    impact=impact,
                    latency_per_agent=1,
                    failure_risk=1,
                )
            )

            print(
                f"{trust},"
                f"{impact},"
                f"{agents}"
            )


if __name__ == "__main__":
    run()
