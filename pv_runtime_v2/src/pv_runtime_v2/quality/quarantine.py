class Quarantine:

    @staticmethod
    def active_agents(
        agents,
        threshold: float = 0.20,
    ):

        return [
            agent
            for agent in agents
            if agent.trust >= threshold
        ]
