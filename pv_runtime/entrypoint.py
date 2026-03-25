"""
CONTROLLED ENTRYPOINT - ADD AUDIT LAYER
"""

from pv_core.identity.identity_service import resolve
from pv_core.simulation.simulator import run
from pv_core.policy.policy_service import evaluate
from pv_core.risk.risk_service import score
from pv_core.enforcement.enforcement_service import enforce
from pv_core.audit.audit_service import log


def execute(intent, agent_id):
    identity = resolve(agent_id)

    sim_input = intent if isinstance(intent, str) else "gpt"
    simulation = run(sim_input)

    risk = score(intent, simulation)
    decision = evaluate(intent, {**simulation, "risk": risk})

    enforcement = enforce(intent, decision)

    payload = {
        "identity": identity,
        "intent": intent,
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
