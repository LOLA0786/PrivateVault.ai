from audit_logger import log_audit_event

def log_pii_event(result):

    event = {
        "event_type": "pii_runtime_enforcement",
        "decision": result["decision"],
        "reason": result["reason"],
        "pii_count": result["count"],
        "pii_types": sorted(
            set(
                x["type"]
                for x in result["findings"]
            )
        )
    }

    log_audit_event(event)

    return event
