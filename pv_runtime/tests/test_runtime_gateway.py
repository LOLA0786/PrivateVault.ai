from pv_runtime.models.runtime_context import RuntimeContext
from pv_runtime.models.decision import Decision
from pv_runtime.models.approval import Approval

from pv_runtime.runtime_gateway import execute


ctx = RuntimeContext(
    agent_id="gateway-test",

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
        allowed=True,
        reason="unit-test",
    ),

    approval=Approval(
        approved=True,
    ),

    runtime_security={},
)

result = execute(ctx)

print(result)

assert result["status"] == "SUCCESS"

print("PASS")
