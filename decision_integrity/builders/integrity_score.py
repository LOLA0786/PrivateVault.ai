def calculate_integrity_score(snapshot):

    score = 100.0

    if snapshot.trust_score < 0.90:
        score -= 10

    if snapshot.trust_score < 0.75:
        score -= 20

    if len(snapshot.tools_requested) != len(snapshot.tools_authorized):
        score -= 15

    if snapshot.policy_context_conflict:
        score -= 25

    if snapshot.retrieval_poisoning_detected:
        score -= 40

    if snapshot.memory_poisoning_detected:
        score -= 40

    if score < 0:
        score = 0

    return round(score, 2)
