from memory_governance.snapshots.memory_snapshot import (
    create_snapshot
)

memory = {
    "fact": "customer_risk=low"
}

snapshot = create_snapshot(
    memory
)

assert "snapshot_id" in snapshot
assert "snapshot_hash" in snapshot

print(
    "SNAPSHOT:",
    snapshot["snapshot_hash"][:16]
)

print("PASS")
