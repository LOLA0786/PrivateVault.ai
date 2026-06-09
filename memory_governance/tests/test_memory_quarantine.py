from memory_governance.quarantine.memory_quarantine import (
    MemoryQuarantine
)

q = MemoryQuarantine()

q.quarantine(
    "mem_001",
    "POISONING_DETECTED"
)

assert q.is_quarantined(
    "mem_001"
)

q.restore(
    "mem_001"
)

assert not q.is_quarantined(
    "mem_001"
)

print("PASS")
