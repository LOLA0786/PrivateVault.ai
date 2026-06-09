import random

from pv_runtime_v2.quality.trust_weighted_vote import Agent


class AgentGenerator:

    def generate(
        self,
        n: int,
    ):

        return [
            Agent(
                trust=random.uniform(
                    0.3,
                    0.95,
                )
            )
            for _ in range(n)
        ]
