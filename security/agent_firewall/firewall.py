from .detector import detect_risk
from .classifier import classify
from .responder import respond
from .anomaly import update_history

def firewall_check(action: str):
    flags = detect_risk(action)
    severity = classify(flags, action)
    decision = respond(action, severity, flags)

    if decision == "ALLOW":
        update_history(action)

    return {
        "action": action,
        "flags": flags,
        "severity": severity,
        "decision": decision
    }
