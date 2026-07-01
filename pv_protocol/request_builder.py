"""
Protocol -> RuntimeContext builder.
"""

from pv_protocol.action_request import ActionRequest

from pv_runtime.models.runtime_context import RuntimeContext
from pv_runtime.models.decision import Decision
from pv_runtime.models.approval import Approval
from approval_binding import expected_approval_hash


def build_runtime_context(
    request: ActionRequest,
) -> RuntimeContext:
    """
    Temporary protocol builder.

    Later this will invoke the real Decision Engine.
    """

    return RuntimeContext(

        agent_id=request.agent.agent_id,

        identity=dict(request.agent.identity),

        tenant={
            "tenant_id": request.agent.tenant_id,
        },

        intent=dict(request.proposal.intent),

        context=dict(request.context),

        decision=Decision(
            allowed=True,
            reason="protocol",
            risk_score=0.0,
        ),

        approval=Approval(
            approved=True,
            intent_hash=expected_approval_hash(
                dict(request.proposal.intent)
            ),
        ),
    )
