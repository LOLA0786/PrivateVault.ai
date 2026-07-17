from datetime import UTC, datetime
import uuid

from pv_protocol.runtime.decision_engine import DecisionEngine
from pv_protocol.models.action_request import (
    ActionRequest,
    Principal,
    Loop,
    Goal,
    ProposedAction,
    Intent,
    GraphRef,
    Limits,
)


class PrivateVaultDecisionAgent:

    def __init__(self, inner_agent):
        self.inner = inner_agent
        self.engine = DecisionEngine()

    async def execute(self, user_query: str, **kwargs):

        request = ActionRequest(
            protocol_version="0.1",
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now(UTC).isoformat(),

            principal=Principal(
                tenant_id="arksim",
                actor_id="synthetic-user",
                actor_type="simulator",
            ),

            loop=Loop(
                loop_id=await self.inner.get_chat_id(),
                iteration=1,
            ),

            goal=Goal(
                goal_id="conversation",
                description="Continue simulated conversation",
                goal_hash="conversation",
            ),

            proposed_action=ProposedAction(
                action_type="agent.respond",
                target="conversation",
                parameters={"query": user_query},
            ),

            intent=Intent(
                description=user_query,
            ),

            graph_ref=GraphRef(
                graph_id="arksim",
                version="1",
                from_node="user",
                to_node="agent",
                edge_id="conversation",
            ),

            limits=Limits(
                max_cost_usd=1.0,
                deadline_ms=5000,
                max_iterations=100,
            ),
        )

        receipt = self.engine.evaluate(request)

        print("\nDecisionReceipt")
        print(receipt)

        if receipt.status != "approved":
            return f"[BLOCKED] {receipt.reason_code}"

        return await self.inner.execute(user_query, **kwargs)
