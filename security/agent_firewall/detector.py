def detect_risk(action: str):
    flags = []

    action_lower = action.lower()

    if "transfer" in action_lower or "payment" in action_lower:
        flags.append({"type": "financial", "severity": "HIGH"})

    if "delete" in action_lower or "drop" in action_lower:
        flags.append({"type": "destructive", "severity": "HIGH"})

    if "scrape" in action_lower or "crawl" in action_lower:
        flags.append({"type": "suspicious", "severity": "MEDIUM"})

    if "admin" in action_lower:
        flags.append({"type": "privilege_escalation", "severity": "HIGH"})

    return flags
