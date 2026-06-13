from pv_runtime.adversarial.runtime_hook import (
    evaluate_adversarial_risk
)

evaluate_adversarial_risk(
    principal="evil_agent",
    action={"action":"step1"},
    text="birch reduction",
    history=[],
    agent_chain=["a"]
)

evaluate_adversarial_risk(
    principal="evil_agent",
    action={"action":"step2"},
    text="reductive amination",
    history=[],
    agent_chain=["a"]
)

print("PASS")
