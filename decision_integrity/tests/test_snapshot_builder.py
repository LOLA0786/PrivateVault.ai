import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import (
    build_snapshot,
    snapshot_hash
)

s = build_snapshot(
    actor_id="user-1",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v1",
    policy_hash="abc123",
)

print("decision_id:", s.decision_id)
print("intent_hash:", s.intent_hash[:16])
print("snapshot_hash:", snapshot_hash(s)[:16])
print("PASS")
