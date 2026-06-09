from memory_governance.trust.memory_trust import (
    calculate_memory_trust,
    trusted,
)

score = calculate_memory_trust(
    provenance_score=100,
    age_score=100,
    usage_score=100,
    contradiction_score=100,
    human_validation_score=100,
)

print("SCORE:", score)

assert score == 100.0
assert trusted(score)

print("PASS")
