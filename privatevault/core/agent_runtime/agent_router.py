class AgentRouter:
    """
    Routes agent actions to tools or other agents
    while preserving governance enforcement.
    """

    def __init__(self, policy_engine, tool_gateway, agent_registry, audit_logger):
        self.policy_engine = policy_engine
        self.tool_gateway = tool_gateway
        self.agent_registry = agent_registry
        self.audit_logger = audit_logger

    def route(self, action):

        # policy check
        allowed = self.policy_engine.evaluate(action)

        if not allowed:
            raise Exception("Policy blocked action")

        target = action.tool

        # agent to agent
        if target.startswith("agent:"):
            agent_name = target.split("agent:")[1]

            if agent_name not in self.agent_registry:
                raise Exception(f"Agent not found: {agent_name}")

            result = self.agent_registry[agent_name].handle(action.parameters)

        else:
            # agent to tool
            result = self.tool_gateway.execute(action)

        self.audit_logger.log(action, result)

        return result
