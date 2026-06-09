import random

from pv_runtime_v2.quality.ground_truth import (
    GroundTruthGenerator,
)

from pv_runtime_v2.quality.byzantine_generator import (
    ByzantineGenerator,
)

from pv_runtime_v2.quality.trust_weighted_vote import (
    TrustWeightedVote,
)

from pv_runtime_v2.quality.trust_updater import (
    TrustUpdater,
)

from pv_runtime_v2.quality.quarantine import (
    Quarantine,
)


def run_trial(
    seed: int,
    byzantine_ratio: float,
):

    random.seed(seed)

    tasks = (
        GroundTruthGenerator()
        .generate(10000)
    )

    voter = (
        TrustWeightedVote()
    )

    agents = (
        ByzantineGenerator()
        .generate(
            77,
            byzantine_ratio,
        )
    )

    correct = 0

    for task in tasks:

        active_agents = (
            Quarantine.active_agents(
                agents
            )
        )

        if len(active_agents) == 0:
            active_agents = agents

        result, decisions = (
            voter.decide(
                task.truth,
                task.difficulty,
                active_agents,
            )
        )

        if result == task.truth:
            correct += 1

        for agent, decision in decisions:

            agent.trust = (
                TrustUpdater.update(
                    agent.trust,
                    decision == task.truth,
                )
            )

    return correct / len(tasks)


def benchmark(
    byzantine_ratio: float,
):

    results = []

    for seed in range(30):

        results.append(
            run_trial(
                seed,
                byzantine_ratio,
            )
        )

    mean = (
        sum(results)
        / len(results)
    )

    print(
        f"byzantine={byzantine_ratio:.2f} "
        f"accuracy={mean:.4f}"
    )


def run():

    benchmark(0.00)
    benchmark(0.10)
    benchmark(0.20)
    benchmark(0.33)
    benchmark(0.40)


if __name__ == "__main__":
    run()
