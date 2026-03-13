from .action_schema import AgentAction


class AgentKernel:
    """
    Central execution pipeline for all agents.
    No agent can bypass this runtime.
    """

    def __init__(self, policy_engine, tool_gateway, audit_logger):
        self.policy_engine = policy_engine
        self.tool_gateway = tool_gateway
        self.audit_logger = audit_logger

    def execute(self, action: AgentAction):

        # 1 policy check
        allowed = self.policy_engine.evaluate(action)

        if not allowed:
            raise Exception("Policy violation")

        # 2 tool execution
        result = self.tool_gateway.execute(action)

        # 3 audit
        self.audit_logger.log(action, result)

        return result
