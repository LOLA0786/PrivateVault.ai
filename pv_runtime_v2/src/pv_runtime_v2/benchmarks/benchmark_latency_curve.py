from pv_runtime_v2.economics.swarm_optimizer import (
    SwarmOptimizer,
)


def run():

    optimizer = SwarmOptimizer()

    print(
        "latency,optimal_agents,utility"
    )

    for latency in [

        0.1,
        0.5,
        1,
        2,
        5,
        10,
        20,
        50,
    ]:

        agents, utility = (
            optimizer.optimal_size(
                trust=0.95,
                impact=10000,
                latency_per_agent=latency,
                failure_risk=1,
            )
        )

        print(
            f"{latency},"
            f"{agents},"
            f"{utility:.2f}"
        )


if __name__ == "__main__":
    run()
