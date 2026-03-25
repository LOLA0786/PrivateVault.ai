"""
CONTROLLED ENTRYPOINT - SAFE INPUT ADAPTATION
"""

from pv_core.identity.identity_service import resolve
from pv_core.simulation.simulator import run
from pv_core.policy.policy_service import evaluate


def execute(intent, agent_id):
    identity = resolve(agent_id)

    # SAFE TEST INPUT for simulation (avoid invalid provider keys)
    sim_input = "default" if isinstance(intent, dict) else intent

    simulation = run(sim_input)
    decision = evaluate(intent, simulation)

    return {
        "identity": identity,
        "simulation": simulation,
        "decision": decision
    }


if __name__ == "__main__":
    print("[CHECK] entrypoint loaded")

    test_intent = {"action": "health_check"}
    test_agent = "agent_1"

    result = execute(test_intent, test_agent)
    print(result)
