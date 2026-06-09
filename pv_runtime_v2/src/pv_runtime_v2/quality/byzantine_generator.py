import random

from pv_runtime_v2.quality.agent import Agent


class ByzantineGenerator:

    def generate(
        self,
        n: int,
        byzantine_ratio: float,
    ):

        agents = []

        byzantine_count = int(
            n * byzantine_ratio
        )

        for i in range(n):

            agents.append(
                Agent(
                    trust=random.uniform(
                        0.3,
                        0.95,
                    ),
                    is_byzantine=(
                        i < byzantine_count
                    ),
                )
            )

        random.shuffle(agents)

        return agents
