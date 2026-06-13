from pv_runtime.adversarial.runtime_escalation import (
    escalation_decision
)

def enforce_adversarial_risk(payload):

    adversarial = payload.get(
        "adversarial",
        {}
    )

    score = adversarial.get(
        "total_score",
        0
    )

    decision = escalation_decision(score)

    if decision == "BLOCK":
        raise Exception(
            "ADVERSARIAL_BEHAVIOR_DETECTED"
        )

    payload["adversarial_decision"] = decision

    return True
