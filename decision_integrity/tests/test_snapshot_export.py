import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import build_snapshot
from decision_integrity.builders.context_integrity import add_context
from decision_integrity.replay.decision_snapshot_export import (
    export_snapshot,
    load_snapshot
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
    content="loan policy",
    source="policy_repo",
    trust_score=0.99
)

path = export_snapshot(
    s,
    "decision_integrity/snapshots/demo_snapshot.json"
)

loaded = load_snapshot(path)

print("decision_id:", loaded["decision_id"])
print("contexts:", len(loaded["context_hashes"]))
print("PASS")
