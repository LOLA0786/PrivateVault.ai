import json
import uuid
import hashlib


def create_snapshot(
    memory
):
    payload = json.dumps(
        memory,
        sort_keys=True
    )

    snapshot_hash = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    return {
        "snapshot_id": str(uuid.uuid4()),
        "snapshot_hash": snapshot_hash,
        "memory": memory,
    }
