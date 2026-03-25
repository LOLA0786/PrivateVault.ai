"""
SAFE WRAPPER - EXPLAINABILITY RECEIPTS
"""

import uuid
import datetime


def generate_receipt(payload):
    receipt = {
        "receipt_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "intent": payload.get("intent"),
        "decision": payload.get("decision"),
        "risk": payload.get("risk"),
        "simulation": payload.get("simulation"),
        "enforcement": payload.get("enforcement"),
        "replay": payload.get("replay"),
        "status": "SUCCESS" if payload.get("decision", {}).get("allowed") else "BLOCKED"
    }

    return receipt


if __name__ == "__main__":
    print(generate_receipt({"test": True}))
