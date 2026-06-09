import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import build_snapshot
from decision_integrity.builders.context_integrity import (
    add_context,
    context_integrity_score
)

s = build_snapshot(
    actor_id="user-1",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v1",
    policy_hash="abc123",
)

add_context(
    s,
    content="Loan policy document",
    source="policy_repo",
    trust_score=0.99
)

add_context(
    s,
    content="Random wiki page",
    source="external",
    trust_score=0.20
)

print("contexts:", len(s.context_hashes))
print("context_score:", context_integrity_score(s))
print("PASS")
