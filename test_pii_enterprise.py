from security.pii.runtime_governance import govern_response
from security.pii.pii_audit_bridge import log_pii_event
from security.pii.pii_ledger_bridge import log_pii_decision

sample = {
    "choices": [{
        "message": {
            "content": """
Rahul Sharma
Email rahul@gmail.com
Phone 9876543210
PAN ABCDE1234F
"""
        }
    }]
}

result = govern_response(sample)

audit_event = log_pii_event(result)

ledger_entry = log_pii_decision(result)

print("DECISION:", result["decision"])
print("AUDIT:", audit_event["event_type"])
print("LEDGER INDEX:", ledger_entry["index"])
