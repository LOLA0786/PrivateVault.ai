import random

from agents.finance_agent import generate_action as finance
from agents.malicious_agent import generate_action as malicious
from agents.risk_agent import generate_action as risk

from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce
from trust_agent.evidence_logger import log


AGENTS = [finance, malicious, risk]


def run():
    print("\n=== MULTI-AGENT CHAOS TEST ===\n")

    for i in range(10):
        agent = random.choice(AGENTS)
        action = agent()

        intent_hash = bind_intent(action)
        decision, reason = evaluate(action)
        valid = verify(intent_hash, action)
        allowed = enforce(decision, valid)

        log(action, decision, reason, intent_hash)

        print(f"[{i}] {action.get('action')} | ${action.get('amount',0)} → {decision} → {'✅' if allowed else '🚫'}")


if __name__ == "__main__":
    run()
