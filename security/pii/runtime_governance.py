from security.pii.runtime_filter import enforce
from security.pii.runtime_policy import evaluate

def govern_response(response):

    pii_result = enforce(response)

    policy = evaluate(
        pii_result["findings"]
    )

    return {
        "response": pii_result["response"],
        "findings": pii_result["findings"],
        "count": pii_result["count"],
        "decision": policy["decision"],
        "reason": policy["reason"]
    }
