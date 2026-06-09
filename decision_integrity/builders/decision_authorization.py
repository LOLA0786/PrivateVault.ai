from decision_integrity.builders.integrity_score import (
    calculate_integrity_score
)


MIN_DECISION_INTEGRITY_SCORE = 80.0


def authorize_decision(snapshot):

    score = calculate_integrity_score(snapshot)

    snapshot.decision_integrity_score = score

    if snapshot.retrieval_poisoning_detected:
        snapshot.outcome = "BLOCKED"
        return False

    if snapshot.memory_poisoning_detected:
        snapshot.outcome = "BLOCKED"
        return False

    if snapshot.policy_context_conflict:
        snapshot.outcome = "BLOCKED"
        return False

    if score < MIN_DECISION_INTEGRITY_SCORE:
        snapshot.outcome = "BLOCKED"
        return False

    snapshot.outcome = "AUTHORIZED"
    return True
