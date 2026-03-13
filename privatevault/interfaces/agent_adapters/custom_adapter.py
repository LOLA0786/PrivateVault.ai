from .base_adapter import BaseAgentAdapter


class CustomAgentAdapter(BaseAgentAdapter):
    """
    Adapter for internal or experimental agents
    """

    def convert(self, data):

        intent = data.get("intent")
        tool = data.get("tool")
        parameters = data.get("params", {})

        return self.to_action(intent, tool, parameters)
