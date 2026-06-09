import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from decision_integrity.builders.snapshot_builder import (
    build_snapshot
)

from decision_integrity.replay.decision_snapshot_export import (
    export_snapshot
)

from decision_integrity.replay.replay_verifier import (
    verify_snapshot
)

s = build_snapshot(
    actor_id="user",
    agent_id="loan-agent",
    intent_text="approve loan",
    policy_version="v17",
    policy_hash="policy17"
)

s.outcome = "AUTHORIZED"

path = export_snapshot(
    s,
    "decision_integrity/snapshots/replay_test.json"
)

r = verify_snapshot(path)

print("decision_id:", r["decision_id"])
print("outcome:", r["outcome"])
print("snapshot_hash:", r["snapshot_hash"][:16])

print("PASS")
