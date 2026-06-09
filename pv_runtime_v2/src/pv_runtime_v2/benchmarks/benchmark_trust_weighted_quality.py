import random

from pv_runtime_v2.quality.ground_truth import (
    GroundTruthGenerator,
)

from pv_runtime_v2.quality.agent_generator import (
    AgentGenerator,
)

from pv_runtime_v2.quality.trust_weighted_vote import (
    TrustWeightedVote,
)

from pv_runtime_v2.quality.variance import (
    VarianceReport,
)


def run_trial(
    seed: int,
    n_tasks: int = 10000,
):

    random.seed(seed)

    tasks = (
        GroundTruthGenerator()
        .generate(n_tasks)
    )

    voter = (
        TrustWeightedVote()
    )

    generator = (
        AgentGenerator()
    )

    correct = 0

    for task in tasks:

        agents = (
            generator.generate(80)
        )

        result = voter.decide(
            task.truth,
            task.difficulty,
            agents,
        )

        if result == task.truth:
            correct += 1

    return correct / len(tasks)


def run():

    results = []

    for seed in range(30):

        results.append(
            run_trial(seed)
        )

    stats = (
        VarianceReport
        .summarize(results)
    )

    print(
        f"mean={stats['mean']:.4f}"
    )

    print(
        f"std={stats['std']:.4f}"
    )

    print(
        f"min={stats['min']:.4f}"
    )

    print(
        f"max={stats['max']:.4f}"
    )


if __name__ == "__main__":
    run()
