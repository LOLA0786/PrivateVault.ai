"""
SAFE WRAPPER - APPROVAL LAYER
"""

def requires_approval(intent, risk, decision):
    if not decision.get("allowed"):
        return False

    if isinstance(intent, dict):
        amount = intent.get("amount", 0)
        if amount and amount > 10000:
            return True

    if risk.get("risk_level") in ["medium", "high"]:
        return True

    return False


def request_approval(payload):
    return {
        "approval_required": True,
        "status": "PENDING",
        "approver": "human_required"
    }


def process(payload):
    if requires_approval(
        payload.get("intent"),
        payload.get("risk", {}),
        payload.get("decision", {})
    ):
        return request_approval(payload)

    return {"approval_required": False}
