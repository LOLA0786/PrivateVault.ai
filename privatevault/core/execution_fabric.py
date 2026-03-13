class ExecutionFabric:
    """
    Central execution layer that coordinates:
    - agent → agent calls
    - agent → tool calls
    - governance checks
    - evidence logging
    """

    def __init__(self, router, policy_engine, tool_gateway, evidence_engine, monitor):
        self.router = router
        self.policy_engine = policy_engine
        self.tool_gateway = tool_gateway
        self.evidence_engine = evidence_engine
        self.monitor = monitor

    def execute(self, action):

        # 1. Governance check
        allowed = self.policy_engine.evaluate(action)
        if not allowed:
            raise Exception("Policy blocked execution")

        # 2. Route execution
        result = self.router.route(action)

        # 3. Evidence record
        self.evidence_engine.record(action, result)
        self.monitor.emit("agent_execution", action)

        return result
