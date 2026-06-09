import random

from pv_runtime_v2.economics.adaptive_swarm import (
    AdaptiveSwarm,
)


def run():

    swarm = AdaptiveSwarm()

    static_agents = 200

    adaptive_total = 0

    for _ in range(1000):

        result = swarm.allocate(
            trust=random.uniform(
                0.2,
                0.95,
            ),
            impact=random.choice(
                [
                    100,
                    1000,
                    10000,
                    100000,
                ]
            ),
            latency_ms=random.choice(
                [
                    0.5,
                    1,
                    2,
                    5,
                ]
            ),
            failure_risk=random.choice(
                [
                    1,
                    5,
                    10,
                    20,
                ]
            ),
        )

        adaptive_total += (
            result[
                "optimal_agents"
            ]
        )

    adaptive_avg = (
        adaptive_total / 1000
    )

    print(
        f"static={static_agents}"
    )

    print(
        f"adaptive_avg="
        f"{adaptive_avg:.2f}"
    )

    savings = (
        (
            static_agents
            - adaptive_avg
        )
        / static_agents
    ) * 100

    print(
        f"savings="
        f"{savings:.2f}%"
    )


if __name__ == "__main__":
    run()
