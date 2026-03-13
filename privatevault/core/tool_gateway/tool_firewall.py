class ToolFirewall:
    """
    Enforces governance rules before tools execute.
    """

    def __init__(self, policy_engine):
        self.policy_engine = policy_engine

    def validate(self, action):
        allowed = self.policy_engine.evaluate(action)

        if not allowed:
            raise Exception("Tool execution blocked by policy")

        return True
