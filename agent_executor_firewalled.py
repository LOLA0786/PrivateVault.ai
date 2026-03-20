from security.agent_firewall.firewall import firewall_check

def real_execute(action: str):
    # TEMP: replace this with actual system call later
    print(f"⚙️ Executing real action: {action}")
    return {"status": "executed", "action": action}

def execute_action(action: str):
    fw = firewall_check(action)

    if fw["decision"] == "BLOCK":
        return {"status": "blocked", "fw": fw}

    if fw["decision"] == "QUARANTINE":
        return {"status": "quarantined", "fw": fw}

    return real_execute(action)
