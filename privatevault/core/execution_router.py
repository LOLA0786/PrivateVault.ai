class ExecutionRouter:

    def __init__(self, agent_registry, tool_gateway):
        self.agent_registry = agent_registry
        self.tool_gateway = tool_gateway

    def route(self, action):

        target = action.tool

        # agent → agent call
        if target.startswith("agent:"):
            name = target.split("agent:")[1]
            agent = self.agent_registry.get(name)
            return agent.handle(action.parameters)

        # agent → external tool
        return self.tool_gateway.execute(action)
