from dataclasses import dataclass
import random


@dataclass(slots=True,frozen=True)
class DecisionTask:

    task_id: int

    truth: bool

    difficulty: float

    impact: float


class GroundTruthGenerator:

    def generate(
        self,
        n: int,
    ):

        tasks = []

        for i in range(n):

            tasks.append(
                DecisionTask(
                    task_id=i,
                    truth=random.choice(
                        [True, False]
                    ),
                    difficulty=random.uniform(
                        0.1,
                        0.9,
                    ),
                    impact=random.choice(
                        [
                            100,
                            1000,
                            10000,
                            100000,
                        ]
                    ),
                )
            )

        return tasks
