"""
CONTROLLED ENTRYPOINT - ADD RISK LAYER
"""

from pv_core.identity.identity_service import resolve
from pv_core.simulation.simulator import run
from pv_core.policy.policy_service import evaluate
from pv_core.risk.risk_service import score


def execute(intent, agent_id):
    identity = resolve(agent_id)

    sim_input = intent if isinstance(intent, str) else "gpt"
    simulation = run(sim_input)

    risk = score(intent, simulation)
    decision = evaluate(intent, {**simulation, "risk": risk})

    return {
        "identity": identity,
        "simulation": simulation,
        "risk": risk,
        "decision": decision
    }


if __name__ == "__main__":
    print("[CHECK] entrypoint loaded")

    test_intent = {"action": "health_check"}
    test_agent = "agent_1"

    result = execute(test_intent, test_agent)
    print(result)
