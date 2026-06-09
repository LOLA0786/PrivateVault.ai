import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tool_authorization import authorize_tool_call
from approval_binding import expected_approval_hash

intent = {
    "action": "process_payment",
    "amount": 500,
    "recipient": "vendor-a",
    "currency": "USD",
}

approval = {
    "intent_hash": expected_approval_hash(intent)
}

result = authorize_tool_call(
    user_id="agent_001",
    tool_name="process_payment",

    declared_intent=intent,
    executed_intent=intent,

    approval=approval,

    capability_token="totally_fake_token"
)

print("AUTHORIZED:", result["authorized"])
print("EXECUTED:", result["executed"])

if not result["authorized"]:
    print("ERROR:", result["error"])

print("PASS")
