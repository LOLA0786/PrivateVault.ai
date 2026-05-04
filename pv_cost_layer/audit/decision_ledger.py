import json
import os
import hashlib
import time

LEDGER_PATH = "pv_cost_layer/audit/decision_ledger.jsonl"


def _hash(obj: dict) -> str:
    s = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(s.encode()).hexdigest()


def _last_hash() -> str:
    if not os.path.exists(LEDGER_PATH):
        return "GENESIS"

    try:
        with open(LEDGER_PATH, "r") as f:
            lines = f.readlines()
            if not lines:
                return "GENESIS"
            last = json.loads(lines[-1])
            return last.get("entry_hash", "GENESIS")
    except Exception:
        return "GENESIS"


def append(entry: dict) -> dict:
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)

    prev = _last_hash()
    entry = dict(entry)
    entry["ts"] = int(time.time() * 1000)
    entry["prev_hash"] = prev
    entry_hash = _hash(entry)
    entry["entry_hash"] = entry_hash

    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    return {"entry_hash": entry_hash, "prev_hash": prev}
