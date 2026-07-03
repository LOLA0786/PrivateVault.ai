import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from jwt_capability import issue_jwt_cap
from tool_authorization import authorize_tool_call
from approval_binding import expected_approval_hash

declared = {
    "action": "process_payment",
    "amount": 500,
    "recipient": "vendor-a",
    "currency": "USD",
}

executed = {
    "action": "process_payment",
    "amount": 5000,
    "recipient": "vendor-a",
    "currency": "USD",
}

approval = {
    "intent_hash": expected_approval_hash(declared)
}

token = issue_jwt_cap(
    decision_id="decision-002",
    action="process_payment",
    principal="agent_001",
)

evidence = {
    "user_request": {
        "canonical": "vendor-a",
        "amount": 500,
    },
    "planner_output": {
        "canonical": "vendor-a",
        "amount": 500,
    },
    "tool_parameters": {
        "canonical": "vendor-a",
        "amount": 5000,
    },
    "enterprise_state": {
        "canonical": "vendor-a",
        "amount": 500,
    },
    "approval": {
        "canonical": "vendor-a",
    },
    "capability": {
        "canonical": "vendor-a",
    },
}

result = authorize_tool_call(
    user_id="agent_001",
    tool_name="process_payment",
    declared_intent=declared,
    executed_intent=executed,
    approval=approval,
    capability_token=token,
    evidence=evidence,
)

print(result)

assert result["authorized"] is False

print("PASS")
