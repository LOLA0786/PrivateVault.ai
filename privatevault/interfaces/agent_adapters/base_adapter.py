from privatevault.core.agent_runtime.action_schema import AgentAction
import time


class BaseAgentAdapter:
    """
    Converts external agent actions into UAAL format.
    """

    def __init__(self, agent_id):
        self.agent_id = agent_id

    def to_action(self, intent, tool, parameters, risk_level="medium"):
        return AgentAction(
            agent_id=self.agent_id,
            intent=intent,
            tool=tool,
            parameters=parameters,
            risk_level=risk_level,
            timestamp=time.time()
        )
