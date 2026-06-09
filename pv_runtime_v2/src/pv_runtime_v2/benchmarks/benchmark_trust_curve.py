from pv_runtime_v2.economics.swarm_optimizer import (
    SwarmOptimizer,
)


def run():

    optimizer = SwarmOptimizer()

    print(
        "trust,optimal_agents,utility"
    )

    for trust in [

        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
        0.75,
        0.80,
        0.85,
        0.90,
        0.95,
    ]:

        agents, utility = (
            optimizer.optimal_size(
                trust=trust,
                impact=10000,
                latency_per_agent=1,
                failure_risk=1,
            )
        )

        print(
            f"{trust},"
            f"{agents},"
            f"{utility:.2f}"
        )


if __name__ == "__main__":
    run()
