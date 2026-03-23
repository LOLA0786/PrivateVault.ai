import json
from datetime import datetime

LOG_FILE = "evidence.jsonl"

def log(action, decision, reason, intent_hash):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "decision": decision,
        "reason": reason,
        "intent_hash": intent_hash
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


def export_jsonl():
    print(f"Logs written to {LOG_FILE}")
