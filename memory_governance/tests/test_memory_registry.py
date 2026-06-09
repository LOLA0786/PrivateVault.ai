from memory_governance.registry.memory_registry import (
    MemoryRegistry,
    MemoryRecord,
)

registry = MemoryRegistry()

record = MemoryRecord(
    memory_id="mem_001",
    memory_hash="abc123",
    source="user_input",
    creator="user",
    trust_score=95.0,
    snapshot_id="snap_001",
    status="ACTIVE",
    created_at="2026-06-09",
)

registry.register(record)

assert registry.exists("mem_001")
assert registry.get("mem_001").trust_score == 95.0

print("PASS")
