from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce
from trust_agent.evidence_logger import log, export_jsonl


def generate_fragmented_attack():
    return [
        {"action": "transfer_funds", "amount": 20000},
        {"action": "transfer_funds", "amount": 25000},
        {"action": "transfer_funds", "amount": 30000},
        {"action": "transfer_funds", "amount": 40000},
    ]


def run():
    print("\n=== MODULAR ATTACK: FRAGMENTATION ===\n")

    for i, action in enumerate(generate_fragmented_attack(), 1):
        intent_hash = bind_intent(action)
        decision, reason = evaluate(action)
        valid = verify(intent_hash, action)
        allowed = enforce(decision, valid)

        log(action, decision, reason, intent_hash)

        print(f"[TX {i}] ${action['amount']} → {decision} → {'✅' if allowed else '🚫'}")

    export_jsonl()


if __name__ == "__main__":
    run()
