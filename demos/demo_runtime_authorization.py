import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jwt_capability import issue_jwt_cap
from tool_authorization import authorize_tool_call
from approval_binding import expected_approval_hash


def run_case(name, intent, executed, evidence, token):

    approval = {
        "intent_hash": expected_approval_hash(intent)
    }

    result = authorize_tool_call(
        user_id="agent_001",
        tool_name="process_payment",
        declared_intent=intent,
        executed_intent=executed,
        approval=approval,
        capability_token=token,
        evidence=evidence,
    )

    print("=" * 60)
    print(name)
    print("=" * 60)
    print(result)
    print()


intent = {
    "action": "process_payment",
    "amount": 500,
    "recipient": "vendor-a",
    "currency": "USD",
}

token = issue_jwt_cap(
    "decision-001",
    "process_payment",
    "agent_001",
)

good = {
    "user_request":{"canonical":"vendor-a"},
    "planner_output":{"canonical":"vendor-a"},
    "tool_parameters":{"canonical":"vendor-a"},
    "enterprise_state":{
        "canonical":"vendor-a",
        "invoice_open":True,
        "target_verified":True,
    },
    "approval":{"canonical":"vendor-a"},
    "capability":{"canonical":"vendor-a"},
}

run_case(
    "CASE 1 : VALID PAYMENT",
    intent,
    intent,
    good,
    token,
)

bad_target = dict(good)
bad_target["tool_parameters"]={"canonical":"vendor-b"}

run_case(
    "CASE 2 : OBJECT DRIFT",
    intent,
    intent,
    bad_target,
    issue_jwt_cap("d2","process_payment","agent_001"),
)

bad_state = dict(good)
bad_state["enterprise_state"]={
    "canonical":"vendor-a",
    "invoice_open":False,
    "target_verified":False,
}

run_case(
    "CASE 3 : ENTERPRISE STATE",
    intent,
    intent,
    bad_state,
    issue_jwt_cap("d3","process_payment","agent_001"),
)

run_case(
    "CASE 4 : INVALID CAPABILITY",
    intent,
    intent,
    good,
    "fake_token",
)
