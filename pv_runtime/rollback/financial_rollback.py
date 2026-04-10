def rollback_transfer(action):
    return {
        "status": "ROLLED_BACK",
        "reverse_action": {
            "action": "refund",
            "amount": action.get("amount"),
            "recipient": action.get("recipient")
        }
    }
