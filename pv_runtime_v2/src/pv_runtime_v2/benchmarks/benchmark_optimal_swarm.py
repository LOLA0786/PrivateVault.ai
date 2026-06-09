from pv_runtime_v2.economics.swarm_optimizer import (
    SwarmOptimizer,
)


def scenario(
    name,
    trust,
    impact,
    latency,
    risk,
):

    optimizer = (
        SwarmOptimizer()
    )

    agents, utility = (
        optimizer.optimal_size(
            trust=trust,
            impact=impact,
            latency_per_agent=latency,
            failure_risk=risk,
        )
    )

    print(
        f"{name}: "
        f"optimal_agents={agents} "
        f"utility={utility:.2f}"
    )


if __name__ == "__main__":

    scenario(
        "low_impact",
        trust=0.80,
        impact=100,
        latency=1,
        risk=1,
    )

    scenario(
        "high_impact",
        trust=0.95,
        impact=10000,
        latency=1,
        risk=1,
    )

    scenario(
        "high_latency",
        trust=0.95,
        impact=10000,
        latency=10,
        risk=1,
    )

    scenario(
        "low_trust",
        trust=0.40,
        impact=10000,
        latency=1,
        risk=10,
    )
