from .base_adapter import BaseAgentAdapter


class LangChainAdapter(BaseAgentAdapter):
    """
    Adapter for LangChain agents
    """

    def convert(self, lc_action):

        intent = lc_action.get("log", "unknown")
        tool = lc_action.get("tool")
        parameters = lc_action.get("tool_input", {})

        return self.to_action(intent, tool, parameters)
