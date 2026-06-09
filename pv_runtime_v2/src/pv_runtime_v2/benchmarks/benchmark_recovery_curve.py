import csv
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


def run():

    random.seed(42)

    tasks = (
        GroundTruthGenerator()
        .generate(10000)
    )

    agents = (
        ByzantineGenerator()
        .generate(
            77,
            0.33,
        )
    )

    voter = (
        TrustWeightedVote()
    )

    total_correct = 0

    detection_step = None

    quarantine_step = None

    rows = []

    for step, task in enumerate(
        tasks,
        start=1,
    ):

        active_agents = (
            Quarantine.active_agents(
                agents
            )
        )

        quarantined = (
            len(agents)
            - len(active_agents)
        )

        if (
            detection_step is None
            and quarantined > 0
        ):
            detection_step = step

        if (
            quarantine_step is None
            and quarantined >= 10
        ):
            quarantine_step = step

        result, decisions = (
            voter.decide(
                task.truth,
                task.difficulty,
                active_agents
                if active_agents
                else agents,
            )
        )

        if result == task.truth:
            total_correct += 1

        for agent, decision in decisions:

            agent.trust = (
                TrustUpdater.update(
                    agent.trust,
                    decision == task.truth,
                )
            )

        if step % 100 == 0:

            accuracy = (
                total_correct
                / step
            )

            rows.append(
                [
                    step,
                    quarantined,
                    round(
                        accuracy,
                        4,
                    ),
                ]
            )

    with open(
        "recovery_curve.csv",
        "w",
        newline="",
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "step",
                "quarantined",
                "accuracy",
            ]
        )

        writer.writerows(rows)

    print(
        f"detection_step={detection_step}"
    )

    print(
        f"quarantine_step={quarantine_step}"
    )

    print(
        f"final_accuracy="
        f"{total_correct/len(tasks):.4f}"
    )


if __name__ == "__main__":
    run()
