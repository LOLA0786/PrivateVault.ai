import json

LEDGER_PATH = "pv_cost_layer/audit/decision_ledger.jsonl"


def by_request_id(request_id: str):
    try:
        with open(LEDGER_PATH, "r") as f:
            return [json.loads(line) for line in f if request_id in line]
    except FileNotFoundError:
        return []
