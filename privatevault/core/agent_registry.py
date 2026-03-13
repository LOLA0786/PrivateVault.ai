class AgentRegistry:
    """
    Registry for all agents in the system.
    """

    def __init__(self):
        self._agents = {}

    def register(self, name, agent):
        self._agents[name] = agent

    def get(self, name):
        if name not in self._agents:
            raise Exception(f"Agent not found: {name}")
        return self._agents[name]
