from pv_runtime.adversarial.runtime_hook import (
    evaluate_adversarial_risk
)

text = "рrосеss_payment"   # Cyrillic homoglyphs

result = evaluate_adversarial_risk(
    principal="attacker",
    action={"action":"process_payment"},
    text=text,
    history=[],
    agent_chain=["agent1"]
)

print(result)
