"""
SAFE WRAPPER - SIEM EVENT STREAMING
"""

import json
import datetime


def build_event(payload):
    return {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_type": detect_event_type(payload),
        "tenant": payload.get("tenant", {}).get("tenant_id"),
        "user": payload.get("identity", {}).get("user_id"),
        "action": payload.get("intent", {}).get("action"),
        "risk": payload.get("risk", {}).get("risk_level"),
        "decision": payload.get("decision"),
        "enforcement": payload.get("enforcement"),
    }


def detect_event_type(payload):
    decision = payload.get("decision", {})
    risk = payload.get("risk", {})

    if not decision.get("allowed"):
        return "BLOCK"

    if risk.get("risk_level") in ["high"]:
        return "HIGH_RISK"

    if payload.get("replay") and payload["replay"] != "not_available":
        return "DRIFT"

    return "INFO"


def send_event(event):
    print("\n[SIEM EVENT]")
    print(json.dumps(event, indent=2))


def process(payload):
    event = build_event(payload)

    if event["event_type"] in ["BLOCK", "HIGH_RISK", "DRIFT"]:
        send_event(event)

    return event
