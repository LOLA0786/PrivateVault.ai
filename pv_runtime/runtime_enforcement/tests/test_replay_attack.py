import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from jwt_capability import issue_jwt_cap
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

token = issue_jwt_cap(
    decision_id="decision-003",
    action="process_payment",
    principal="agent_001",
)

evidence = {
    "user_request": {"canonical":"vendor-a"},
    "planner_output": {"canonical":"vendor-a"},
    "tool_parameters": {"canonical":"vendor-a"},
    "enterprise_state": {"canonical":"vendor-a"},
    "approval": {"canonical":"vendor-a"},
    "capability": {"canonical":"vendor-a"},
}

first = authorize_tool_call(
    user_id="agent_001",
    tool_name="process_payment",
    declared_intent=intent,
    executed_intent=intent,
    approval=approval,
    capability_token=token,
    evidence=evidence,
)

second = authorize_tool_call(
    user_id="agent_001",
    tool_name="process_payment",
    declared_intent=intent,
    executed_intent=intent,
    approval=approval,
    capability_token=token,
    evidence=evidence,
)

print(first)
print(second)

assert first["authorized"] is True
assert second["authorized"] is False
assert "REPLAY_DETECTED" in second["error"]

print("PASS")
