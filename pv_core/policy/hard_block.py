def check(intent):
    dangerous = ["rm -rf", "delete_all", "shutdown", "drop_table"]

    intent_str = str(intent).lower()

    for d in dangerous:
        if d in intent_str:
            return {
                "allowed": False,
                "policy": "hard_block",
                "reason": "dangerous_capability"
            }
    return None
