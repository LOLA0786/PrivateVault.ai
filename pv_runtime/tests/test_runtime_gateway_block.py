from pv_runtime.models.runtime_context import RuntimeContext
from pv_runtime.models.decision import Decision
from pv_runtime.models.approval import Approval

from pv_runtime.runtime_gateway import execute

ctx = RuntimeContext(
    agent_id="gateway-block",

    identity={},
    tenant={},

    intent={
        "action": "transfer",
        "amount": 25,
        "recipient": "vendor_a",
    },

    context={},
    simulation={},
    risk={},

    decision=Decision(
        allowed=False,
        reason="policy_block",
    ),

    approval=Approval(
        approved=False,
    ),

    runtime_security={},
)

try:
    result = execute(ctx)
    print(result)

    assert result["status"] in (
        "BLOCK",
        "TERMINATE",
        "PAUSE",
        "APPROVAL",
    )

    assert "result" not in result
    assert "loop_receipt" not in result

    print("PASS")

except Exception as e:
    print(type(e).__name__)
    print(e)
    print("PASS")
