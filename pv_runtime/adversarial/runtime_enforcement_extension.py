def enforce_adversarial_risk(payload):

    adversarial = payload.get(
        "adversarial",
        {}
    )

    score = adversarial.get(
        "total_score",
        0
    )

    if score > 70:

        raise Exception(
            "ADVERSARIAL_BEHAVIOR_DETECTED"
        )

    return True
