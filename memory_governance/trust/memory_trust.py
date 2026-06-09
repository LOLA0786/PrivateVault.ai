def calculate_memory_trust(
    provenance_score=100,
    age_score=100,
    usage_score=100,
    contradiction_score=100,
    human_validation_score=100,
):
    score = (
        provenance_score * 0.25 +
        age_score * 0.15 +
        usage_score * 0.20 +
        contradiction_score * 0.25 +
        human_validation_score * 0.15
    )

    return round(score, 2)


def trusted(
    score,
    threshold=50
):
    return score >= threshold
