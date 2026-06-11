from security.pii.runtime_governance import govern_response
from datetime import datetime, UTC
import json

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

evidence = {
    "timestamp": datetime.now(UTC).isoformat(),
    "control": "PII_RUNTIME_ENFORCEMENT",
    "decision": result["decision"],
    "reason": result["reason"],
    "pii_count": result["count"]
}

print(json.dumps(evidence, indent=2))
