def evaluate(findings):

    count = len(findings)

    if count == 0:
        return {
            "decision": "ALLOW",
            "reason": "NO_PII"
        }

    if count <= 5:
        return {
            "decision": "ALLOW_WITH_REDACTION",
            "reason": "PII_PRESENT"
        }

    return {
        "decision": "DENY",
        "reason": "BULK_PII_EXPORT"
    }
