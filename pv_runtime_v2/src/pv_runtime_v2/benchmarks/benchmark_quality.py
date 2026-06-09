from pv_runtime_v2.quality.ground_truth import (
    GroundTruthGenerator,
)

from pv_runtime_v2.quality.swarm_vote import (
    SwarmVote,
)

from pv_runtime_v2.quality.quality_metrics import (
    QualityMetrics,
)

from pv_runtime_v2.economics.adaptive_swarm import (
    AdaptiveSwarm,
)


def run():

    generator = (
        GroundTruthGenerator()
    )

    voter = (
        SwarmVote()
    )

    adaptive = (
        AdaptiveSwarm()
    )

    tasks = (
        generator.generate(
            10000
        )
    )

    static_correct = 0

    adaptive_correct = 0

    adaptive_agents = 0

    for task in tasks:

        if voter.vote(
            task.truth,
            task.difficulty,
            200,
        ):
            static_correct += 1

        result = (
            adaptive.allocate(
                trust=0.7,
                impact=task.impact,
                latency_ms=1,
                failure_risk=5,
            )
        )

        swarm_size = (
            result[
                "optimal_agents"
            ]
        )

        adaptive_agents += (
            swarm_size
        )

        if voter.vote(
            task.truth,
            task.difficulty,
            swarm_size,
        ):
            adaptive_correct += 1

    print(
        "static_accuracy=",
        round(
            QualityMetrics.accuracy(
                len(tasks),
                static_correct,
            ),
            4,
        ),
    )

    print(
        "adaptive_accuracy=",
        round(
            QualityMetrics.accuracy(
                len(tasks),
                adaptive_correct,
            ),
            4,
        ),
    )

    print(
        "adaptive_avg_agents=",
        round(
            adaptive_agents
            / len(tasks),
            2,
        ),
    )


if __name__ == "__main__":
    run()
