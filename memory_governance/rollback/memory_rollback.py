def rollback_memory(
    memory_store,
    memory_id,
    snapshot
):
    memory_store[memory_id] = snapshot["memory"]

    return memory_store[memory_id]
