from trust_agent.temporal_guard import check as temporal_check

def evaluate(action):
    action_type = action.get("action", "")
    amount = action.get("amount", 0)

    if "command" in action or action_type in ["system_command", "execute_shell"]:
        return "BLOCK", "dangerous_capability"

    if action.get("override") or action.get("bypass_auth"):
        return "BLOCK", "override_detected"

    temporal = temporal_check(action)

    if temporal == "BLOCK":
        return "BLOCK", "temporal_limit"
    elif temporal == "FLAG":
        return "BLOCK", "preemptive_block"
    elif temporal == "BLOCK_SPIKE":
        return "BLOCK", "sudden_spike"

    if amount > 100000:
        return "BLOCK", "high_amount"

    return "ALLOW", "ok"
