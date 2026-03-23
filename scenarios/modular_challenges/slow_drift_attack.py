from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce

def run():
    print("\n=== SLOW DRIFT ATTACK ===\n")

    actions = [10000, 12000, 15000, 18000, 20000]

    for i, amt in enumerate(actions, 1):
        action = {"action": "transfer_funds", "amount": amt}

        intent_hash = bind_intent(action)
        decision, reason = evaluate(action)
        valid = verify(intent_hash, action)
        allowed = enforce(decision, valid)

        print(f"[TX {i}] ${amt} → {decision} ({reason}) → {'✅' if allowed else '🚫'}")

if __name__ == "__main__":
    run()
