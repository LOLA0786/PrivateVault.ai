from uuid import uuid4

from pv_protocol.runtime_adapter import RuntimeAdapter

from pv_protocol.action_request import (
    ActionRequest,
    AgentIdentity,
    Proposal,
)

runtime = RuntimeAdapter()

request = ActionRequest(

    request_id=str(uuid4()),

    agent=AgentIdentity(
        agent_id="protocol-agent",
    ),

    proposal=Proposal(

        intent={
            "action": "transfer",
            "amount": 25,
            "recipient": "vendor_a",
        },

        action={
            "action": "transfer",
            "amount": 25,
            "recipient": "vendor_a",
        },
    ),
)

response = runtime.evaluate(request)

print(response)

assert response.execution.executed
assert response.decision.allowed
assert response.receipt.receipt_hash != ""

print("PASS")
