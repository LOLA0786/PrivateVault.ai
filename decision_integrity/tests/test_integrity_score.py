import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import build_snapshot
from decision_integrity.builders.integrity_score import calculate_integrity_score

s = build_snapshot(
    actor_id="user-1",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v1",
    policy_hash="abc123",
    trust_score=0.95
)

print("score:", calculate_integrity_score(s))

s.policy_context_conflict = True

print("score_after_conflict:", calculate_integrity_score(s))

print("PASS")
