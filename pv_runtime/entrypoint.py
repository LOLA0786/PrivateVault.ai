"""
CONTROLLED ENTRYPOINT - ADD CONTEXT LAYER
"""

from pv_core.intent.intent_service import normalize
from pv_core.context.context_service import build_context
from pv_core.identity.identity_service import resolve
from pv_core.simulation.simulator import run
from pv_core.policy.policy_service import evaluate
from pv_core.risk.risk_service import score
from pv_core.enforcement.enforcement_service import enforce
from pv_core.audit.audit_service import log


def execute(raw_intent, agent_id):
    intent = normalize(raw_intent, agent_id)

    context = build_context(intent)

    identity = resolve(agent_id)

    sim_input = intent if isinstance(intent, str) else "gpt"
    simulation = run(sim_input)

    risk = score(intent, simulation)

    enriched_context = {**context, **simulation, "risk": risk}

    decision = evaluate(intent, enriched_context)

    enforcement = enforce(intent, decision)

    payload = {
        "identity": identity,
        "intent": intent,
        "context": context,
        "simulation": simulation,
        "risk": risk,
        "decision": decision,
        "enforcement": enforcement
    }

    log(payload)

    return payload


if __name__ == "__main__":
    print("[CHECK] entrypoint loaded")

    test_intent = {"action": "health_check"}
    test_agent = "agent_1"

    result = execute(test_intent, test_agent)
    print(result)
