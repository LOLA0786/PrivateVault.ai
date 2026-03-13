class AgentRegistry:
    """
    Registry of all active agents.
    """

    def __init__(self):
        self.agents = {}

    def register(self, name, agent):
        self.agents[name] = agent

    def get(self, name):
        if name not in self.agents:
            raise Exception(f"Agent not registered: {name}")
        return self.agents[name]
