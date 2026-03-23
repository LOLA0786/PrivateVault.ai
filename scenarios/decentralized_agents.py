import random

from agents.weather_agent import generate_action as weather
from agents.finance_agent import generate_action as finance
from agents.risk_agent import generate_action as risk
from agents.malicious_agent import generate_action as malicious
from agents.crime_agent import generate_action as crime
from agents.system_agent import generate_action as system

from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce
from trust_agent.evidence_logger import log


AGENTS = [
    ("Weather", weather),
    ("Finance", finance),
    ("Risk", risk),
    ("Malicious", malicious),
    ("Crime", crime),
    ("System", system),
]


def run():
    print("\n=== TRUE DECENTRALIZED AGENTS ===\n")
    print("No shared memory. No coordination. Different domains.\n")

    random.shuffle(AGENTS)

    for name, fn in AGENTS:
        action = fn()

        intent_hash = bind_intent(action)
        decision, reason = evaluate(action)
        valid = verify(intent_hash, action)
        allowed = enforce(decision, valid)

        log(action, decision, reason, intent_hash)

        print(f"[{name}]")
        print(f"Action: {action}")
        print(f"Decision: {decision} | {reason}")
        print(f"Result: {'✅ ALLOW' if allowed else '🚫 BLOCK'}\n")


if __name__ == "__main__":
    run()
