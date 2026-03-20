from .config import config
import json
import time

LOG_FILE = "logs/firewall/firewall_log.json"

def log_event(event):
    if not config.TELEMETRY_ENABLED:
        return
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")
    except Exception:
        pass

def respond(action, severity, flags):
    event = {
        "timestamp": time.time(),
        "action": action,
        "severity": severity,
        "flags": flags
    }

    if severity == "HIGH":
        event["decision"] = "BLOCK"
        log_event(event)
    if not config.TELEMETRY_ENABLED:
        return
        print(f"🚫 BLOCKED: {action}")
        return "BLOCK"

    elif severity == "MEDIUM":
        event["decision"] = "QUARANTINE"
        log_event(event)
    if not config.TELEMETRY_ENABLED:
        return
        print(f"⚠️ QUARANTINED: {action}")
        return "QUARANTINE"

    else:
        event["decision"] = "ALLOW"
        log_event(event)
    if not config.TELEMETRY_ENABLED:
        return
        print(f"✅ ALLOWED: {action}")
        return "ALLOW"
