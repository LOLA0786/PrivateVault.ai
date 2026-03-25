"""
SAFE WRAPPER - CONNECTOR EXECUTION
"""

def execute_action(intent, decision):
    if not decision.get("allowed"):
        return {
            "executed": False,
            "reason": "blocked_by_policy"
        }

    action = intent.get("action")

    if action == "transfer_funds":
        return {
            "executed": True,
            "status": "SUCCESS",
            "transaction_id": "txn_12345"
        }

    if action == "get_weather":
        return {
            "executed": True,
            "data": "sunny"
        }

    return {
        "executed": True,
        "status": "NO_OP"
    }
