from pv_runtime.entrypoint import execute

from pv_economics.integrations.outcome_bridge import (
    OutcomeBridge
)


class PrivateVaultControlPlane:

    def __init__(self):
        self.outcomes = OutcomeBridge()

    def evaluate(
        self,
        agent_id,
        intent
    ):

        result = execute(
            raw_intent=intent,
            agent_id=agent_id
        )

        return result


control_plane = PrivateVaultControlPlane()
