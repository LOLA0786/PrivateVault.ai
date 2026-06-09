from memory_governance.registry.memory_registry import (
    MemoryRegistry,
    MemoryRecord,
)

from memory_governance.provenance.memory_provenance import (
    assert_provenance,
)

from memory_governance.trust.memory_trust import (
    calculate_memory_trust,
)

from memory_governance.quarantine.memory_quarantine import (
    MemoryQuarantine,
)

from memory_governance.snapshots.memory_snapshot import (
    create_snapshot,
)

from memory_governance.rollback.memory_rollback import (
    rollback_memory,
)

registry = MemoryRegistry()
quarantine = MemoryQuarantine()

memory = {
    "customer_id": "C001",
    "risk": "low",
}

assert_provenance(
    "user_input"
)

score = calculate_memory_trust()

snapshot = create_snapshot(
    memory
)

record = MemoryRecord(
    memory_id="mem_001",
    memory_hash=snapshot["snapshot_hash"],
    source="user_input",
    creator="user",
    trust_score=score,
    snapshot_id=snapshot["snapshot_id"],
    status="ACTIVE",
    created_at="2026-06-09",
)

registry.register(record)

memory_store = {
    "mem_001": memory
}

memory_store["mem_001"] = {
    "customer_id": "C001",
    "risk": "high",
    "injected": True,
}

quarantine.quarantine(
    "mem_001",
    "MEMORY_POISONING"
)

rollback_memory(
    memory_store,
    "mem_001",
    snapshot
)

assert (
    memory_store["mem_001"]["risk"]
    ==
    "low"
)

print(
    "MEMORY_ID:",
    record.memory_id
)

print(
    "TRUST_SCORE:",
    score
)

print(
    "QUARANTINED:",
    quarantine.is_quarantined(
        "mem_001"
    )
)

print(
    "ROLLED_BACK:",
    memory_store["mem_001"]
)

print("PASS")
