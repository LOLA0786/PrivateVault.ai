import json

from trust_agent.intent_binder import bind_intent
from trust_agent.policy_engine import evaluate
from trust_agent.verifier import verify
from trust_agent.firewall import enforce


LOG_FILE = "evidence.jsonl"


def replay():
    print("\n=== REPLAY ENGINE ===\n")

    with open(LOG_FILE, "r") as f:
        for i, line in enumerate(f, 1):
            record = json.loads(line)

            action = record["action"]

            # recompute
            intent_hash = bind_intent(action)
            decision, reason = evaluate(action)
            valid = verify(intent_hash, action)
            allowed = enforce(decision, valid)

            original = record["decision"]
            replayed = decision

            status = "✅ MATCH" if original == replayed else "❌ DRIFT"

            print(f"[{i}] {action}")
            print(f"Original: {original}")
            print(f"Replay  : {replayed} ({reason})")
            print(f"Result  : {status}\n")


if __name__ == "__main__":
    replay()
