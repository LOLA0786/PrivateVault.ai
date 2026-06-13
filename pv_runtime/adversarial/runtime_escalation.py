def escalation_decision(score):

    if score >= 80:
        return "BLOCK"

    if score >= 50:
        return "APPROVAL"

    return "ALLOW"
