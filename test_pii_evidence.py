from security.pii.runtime_governance import govern_response
import json
from datetime import datetime, UTC

sample = {
    "choices": [{
        "message": {
            "content": """
Rahul Sharma
Email: rahul@gmail.com
Phone: 9876543210
PAN: ABCDE1234F
"""
        }
    }]
}

result = govern_response(sample)

evidence = {
    "timestamp": datetime.now(UTC).isoformat(),
    "control": "PII_RUNTIME_ENFORCEMENT",
    "decision": "ALLOW_WITH_REDACTION",
    "pii_count": result["count"],
    "pii_types": sorted(
        set(x["type"] for x in result["findings"])
    )
}

print(json.dumps(evidence, indent=2))
