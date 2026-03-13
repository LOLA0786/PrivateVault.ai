from .tool_registry import ToolRegistry
from .tool_firewall import ToolFirewall


class ToolGateway:
    """
    Secure gateway for executing external tools.
    """

    def __init__(self, policy_engine):
        self.registry = ToolRegistry()
        self.firewall = ToolFirewall(policy_engine)

    def register_tool(self, name, func):
        self.registry.register(name, func)

    def execute(self, action):

        # validate policy
        self.firewall.validate(action)

        # get tool
        tool = self.registry.get(action.tool)

        # execute
        return tool(**action.parameters)
