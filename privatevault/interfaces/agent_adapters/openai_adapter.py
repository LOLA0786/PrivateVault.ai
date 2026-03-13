from .base_adapter import BaseAgentAdapter


class OpenAIAgentAdapter(BaseAgentAdapter):
    """
    Adapter for OpenAI based agents.
    """

    def convert(self, agent_output):
        """
        Convert OpenAI tool call into UAAL action
        """

        intent = agent_output.get("intent")
        tool = agent_output.get("tool")
        parameters = agent_output.get("parameters", {})

        return self.to_action(intent, tool, parameters)
