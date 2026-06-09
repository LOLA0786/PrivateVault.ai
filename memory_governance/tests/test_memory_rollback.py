from memory_governance.snapshots.memory_snapshot import (
    create_snapshot
)

from memory_governance.rollback.memory_rollback import (
    rollback_memory
)

store = {}

store["mem_001"] = {
    "fact": "customer_risk=low"
}

snapshot = create_snapshot(
    store["mem_001"]
)

store["mem_001"] = {
    "fact": "customer_risk=high"
}

rollback_memory(
    store,
    "mem_001",
    snapshot
)

assert (
    store["mem_001"]["fact"]
    ==
    "customer_risk=low"
)

print("PASS")
