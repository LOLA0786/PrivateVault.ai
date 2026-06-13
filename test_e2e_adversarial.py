from pv_runtime.adversarial.runtime_hook import (
    evaluate_adversarial_risk
)

history = [
    "previous step",
    "combine previous step",
    "continue earlier process",
    "next phase"
]

agents = [
    "agent_a",
    "agent_b",
    "agent_a"
]

result = evaluate_adversarial_risk(
    history,
    agents
)

print(result)

print(
    "TOTAL:",
    result["total_score"]
)

