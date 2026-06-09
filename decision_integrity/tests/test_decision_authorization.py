import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import build_snapshot
from decision_integrity.builders.decision_authorization import (
    authorize_decision
)

s1 = build_snapshot(
    actor_id="user-1",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v1",
    policy_hash="abc123",
    trust_score=0.99
)

print("authorized:", authorize_decision(s1))
print("outcome:", s1.outcome)
print("score:", s1.decision_integrity_score)

s2 = build_snapshot(
    actor_id="user-1",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v1",
    policy_hash="abc123",
    trust_score=0.99
)

s2.policy_context_conflict = True

print("authorized_after_conflict:", authorize_decision(s2))
print("outcome_after_conflict:", s2.outcome)
print("score_after_conflict:", s2.decision_integrity_score)

print("PASS")
