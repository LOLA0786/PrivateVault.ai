from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce

def run():
    print("\n=== SPIKE ATTACK TEST ===\n")

    actions = [
        {"action": "transfer_funds", "amount": 10000},
        {"action": "transfer_funds", "amount": 12000},
        {"action": "transfer_funds", "amount": 80000},  # spike
    ]

    for i, action in enumerate(actions, 1):
        intent_hash = bind_intent(action)
        decision, reason = evaluate(action)
        valid = verify(intent_hash, action)
        allowed = enforce(decision, valid)

        print(f"[TX {i}] ${action['amount']} → {decision} ({reason}) → {'✅' if allowed else '🚫'}")

if __name__ == "__main__":
    run()
