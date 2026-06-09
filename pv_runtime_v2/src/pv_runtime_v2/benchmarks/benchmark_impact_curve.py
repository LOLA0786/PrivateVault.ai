from pv_runtime_v2.economics.swarm_optimizer import (
    SwarmOptimizer,
)


def run():

    optimizer = SwarmOptimizer()

    print(
        "impact,optimal_agents,utility"
    )

    for impact in [

        10,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        50000,
        100000,
    ]:

        agents, utility = (
            optimizer.optimal_size(
                trust=0.95,
                impact=impact,
                latency_per_agent=1,
                failure_risk=1,
            )
        )

        print(
            f"{impact},"
            f"{agents},"
            f"{utility:.2f}"
        )


if __name__ == "__main__":
    run()
