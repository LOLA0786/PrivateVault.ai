from pv_runtime_v2.consensus.health_calculator import (
    HealthCalculator,
)

TOTAL_AGENTS = 10000
CLUSTERS = 50

SCENARIOS = [
    500,
    1500,
    3000,
    5000,
    7000,
]


def run():

    calculator = HealthCalculator()

    agents_per_cluster = (
        TOTAL_AGENTS // CLUSTERS
    )

    print()

    for compromised in SCENARIOS:

        compromised_per_cluster = (
            compromised // CLUSTERS
        )

        scores = []

        for cluster in range(CLUSTERS):

            healthy = (
                agents_per_cluster
                - compromised_per_cluster
            )

            state = calculator.evaluate(
                cluster_id=f"c-{cluster}",
                healthy_agents=healthy,
                quarantined_agents=compromised_per_cluster,
            )

            scores.append(
                state.health_score
            )

        avg_health = (
            sum(scores)
            / len(scores)
        )

        governance_alive = (
            avg_health >= 0.67
        )

        print(
            f"compromised={compromised} "
            f"health={avg_health:.2f} "
            f"alive={governance_alive}"
        )


if __name__ == "__main__":
    run()
