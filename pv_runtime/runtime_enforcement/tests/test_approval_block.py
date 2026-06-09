import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tool_authorization import authorize_tool_call
from jwt_capability import issue_jwt_cap

intent = {
    "action": "process_payment",
    "amount": 500,
    "recipient": "vendor-a",
    "currency": "USD",
}

token = issue_jwt_cap(
    "decision-001",
    "process_payment",
    "agent_001"
)

result = authorize_tool_call(
    user_id="agent_001",
    tool_name="process_payment",

    declared_intent=intent,
    executed_intent=intent,

    approval={
        "intent_hash": "tampered_hash"
    },

    capability_token=token
)

print("AUTHORIZED:", result["authorized"])
print("EXECUTED:", result["executed"])

if not result["authorized"]:
    print("ERROR:", result["error"])

print("PASS")
