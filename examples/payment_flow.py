from datetime import UTC, datetime
import uuid

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

from pv_protocol.validator import (
    validate_action_request,
    validate_decision_receipt,
)

from pv_protocol.runtime.decision_engine import DecisionEngine


request = ActionRequest(
    protocol_version="0.1",

    request_id=str(uuid.uuid4()),

    timestamp=datetime.now(UTC).isoformat(),

    principal=Principal(
        tenant_id="acme",
        actor_id="planner-1",
        actor_type="agent"
    ),

    loop=Loop(
        loop_id="loop-001",
        iteration=1
    ),

    goal=Goal(
        goal_id="goal-1",
        description="Pay approved supplier invoice",
        goal_hash="goalhash123"
    ),

    proposed_action=ProposedAction(
        action_type="payment.transfer",
        target="finance.payments",
        parameters={
            "amount": 1200,
            "currency": "USD"
        },
        resource_scope="vendor_account"
    ),

    intent=Intent(
        description="Transfer payment for approved invoice"
    ),

    graph_ref=GraphRef(
        graph_id="graph-001",
        version="1.0",
        from_node="planner",
        to_node="executor",
        edge_id="planner->executor"
    ),

    limits=Limits(
        max_cost_usd=1.25,
        deadline_ms=3000,
        max_iterations=10
    )
)

validate_action_request(request)

engine = DecisionEngine()

receipt = engine.evaluate(request)

validate_decision_receipt(receipt)

print("=" * 60)
print("Decision Runtime Protocol Demo")
print("=" * 60)

print("\nActionRequest\n")
print(request.to_dict())

print("\nDecisionReceipt\n")
print(receipt.to_dict())

print("\n✓ DRP Round Trip Successful")
