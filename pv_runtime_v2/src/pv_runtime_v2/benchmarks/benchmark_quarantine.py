import time

from pv_runtime_v2.consensus.health_calculator import (
    HealthCalculator,
)


TOTAL_AGENTS = 10000
CLUSTERS = 50
COMPROMISED = 500


def run():

    calculator = (
        HealthCalculator()
    )

    compromised_per_cluster = (
        COMPROMISED // CLUSTERS
    )

    agents_per_cluster = (
        TOTAL_AGENTS // CLUSTERS
    )

    start = (
        time.perf_counter()
    )

    health = []

    for cluster in range(CLUSTERS):

        quarantined = (
            compromised_per_cluster
        )

        healthy = (
            agents_per_cluster
            - quarantined
        )

        health.append(
            calculator.evaluate(
                cluster_id=f"c-{cluster}",
                healthy_agents=healthy,
                quarantined_agents=quarantined,
            )
        )

    elapsed = (
        time.perf_counter()
        - start
    ) * 1000

    avg_health = (
        sum(
            h.health_score
            for h in health
        )
        / len(health)
    )

    print(
        f"clusters={CLUSTERS} "
        f"agents={TOTAL_AGENTS} "
        f"compromised={COMPROMISED}"
    )

    print(
        f"avg_health={avg_health:.4f}"
    )

    print(
        f"isolation_time={elapsed:.4f} ms"
    )


if __name__ == "__main__":
    run()
