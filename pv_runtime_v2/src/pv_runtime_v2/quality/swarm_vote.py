import random


class SwarmVote:

    def vote(
        self,
        truth: bool,
        difficulty: float,
        agents: int,
    ):

        correct = 0

        base_accuracy = 0.85

        agent_accuracy = (
            base_accuracy
            - (difficulty * 0.25)
        )

        for _ in range(agents):

            if random.random() < agent_accuracy:
                decision = truth
            else:
                decision = not truth

            if decision == truth:
                correct += 1

        return correct > (agents / 2)
