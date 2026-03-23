from agents.finance_agent import generate_action as finance
from agents.risk_agent import generate_action as risk

from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce
from trust_agent.evidence_logger import log, export_jsonl


def run():
    print("\n=== COORDINATION CHALLENGE: IMPLICIT COLLUSION ===\n")

    # Finance tries large transfer
    tx = finance()
    tx["amount"] = 300000

    # Risk agent tries to reduce perceived risk artificially
    risk_action = risk()
    risk_action["risk_score"] = 0.1  # malicious downgrade
    risk_action["amount"] = tx["amount"]

    for name, action in [("Finance", tx), ("Risk Manipulated", risk_action)]:
        intent_hash = bind_intent(action)
        decision, reason = evaluate(action)
        valid = verify(intent_hash, action)
        allowed = enforce(decision, valid)

        log(action, decision, reason, intent_hash)

        print(f"[{name}] {action.get('action')} | ${action.get('amount',0)}")
        print(f"Decision: {decision} | {reason}")
        print("Result:", "✅" if allowed else "🚫", "\n")

    export_jsonl()


if __name__ == "__main__":
    run()
