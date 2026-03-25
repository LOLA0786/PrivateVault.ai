"""
CONTROLLED ENTRYPOINT - ADD CONNECTORS (REAL EXECUTION)
"""

from pv_core.intent.intent_service import normalize
from pv_core.context.context_service import build_context
from pv_core.iam.iam_service import resolve_identity
from pv_core.tenant.tenant_service import resolve_tenant
from pv_core.simulation.simulator import run
from pv_core.policy.policy_service import evaluate
from pv_core.risk.risk_service import score
from pv_core.enforcement.enforcement_service import enforce
from pv_core.connectors.connector_service import execute_action
from pv_core.audit.audit_service import log
from pv_core.replay.replay_service import replay
from pv_core.explainability.receipt_service import generate_receipt
from pv_core.approval.approval_service import process as approval_process
from pv_core.coordination.coordination_service import (
    start_trace, add_step, finalize_trace
)


def execute(raw_intent, agent_id):
    intent = normalize(raw_intent, agent_id)

    trace = start_trace(agent_id, intent)

    context = build_context(intent)

    identity = resolve_identity(agent_id)
    tenant = resolve_tenant(identity)

    sim_input = intent if isinstance(intent, str) else "gpt"
    simulation = run(sim_input)
    trace = add_step(trace, agent_id, "simulation", "DONE")

    risk = score(intent, simulation)
    trace = add_step(trace, agent_id, "risk_scoring", "DONE")

    enriched_context = {
        **context,
        **simulation,
        "risk": risk,
        "tenant": tenant
    }

    decision = evaluate(intent, enriched_context)
    trace = add_step(trace, agent_id, "policy_evaluation", "DONE")

    approval = approval_process({
        "intent": intent,
        "risk": risk,
        "decision": decision,
        "tenant": tenant
    })
    trace = add_step(trace, agent_id, "approval_check", "DONE")

    enforcement = enforce(identity["user_id"], decision)
    trace = add_step(trace, agent_id, "enforcement", "DONE")

    execution = execute_action(intent, decision)
    trace = add_step(trace, agent_id, "execution", "DONE")

    payload = {
        "identity": identity,
        "tenant": tenant,
        "intent": intent,
        "context": context,
        "simulation": simulation,
        "risk": risk,
        "decision": decision,
        "approval": approval,
        "enforcement": enforcement,
        "execution": execution,
        "trace": trace
    }

    payload["replay"] = replay(payload)
    payload["receipt"] = generate_receipt(payload)

    trace = finalize_trace(trace, decision)
    payload["trace"] = trace

    log(payload)

    return payload


if __name__ == "__main__":
    test_intent = {"action": "transfer_funds", "amount": 20000}
    test_agent = "agent_1"

    result = execute(test_intent, test_agent)
    print(result)
