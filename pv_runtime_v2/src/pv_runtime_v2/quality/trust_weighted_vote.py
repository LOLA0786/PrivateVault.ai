import random

from pv_runtime_v2.quality.agent import Agent


class TrustWeightedVote:

    def decide(
        self,
        truth: bool,
        difficulty: float,
        agents: list[Agent],
    ):

        positive = 0.0
        negative = 0.0

        decisions = []

        for agent in agents:

            if agent.is_byzantine:

                decision = not truth

            else:

                accuracy = (
                    0.55
                    + (agent.trust * 0.4)
                    - (difficulty * 0.25)
                )

                accuracy = max(
                    0.5,
                    min(
                        accuracy,
                        0.99,
                    ),
                )

                if random.random() < accuracy:
                    decision = truth
                else:
                    decision = not truth

            decisions.append(
                (
                    agent,
                    decision,
                )
            )

            if decision:
                positive += agent.trust
            else:
                negative += agent.trust

        final_decision = (
            positive > negative
        )

        return (
            final_decision,
            decisions,
        )
