import json
import hashlib


def sha256(v):
    return hashlib.sha256(
        str(v).encode()
    ).hexdigest()


def verify_snapshot(snapshot_path):

    with open(snapshot_path, "r") as f:
        snapshot = json.load(f)

    payload = json.dumps(
        snapshot,
        sort_keys=True
    )

    snapshot_hash = sha256(
        payload
    )

    return {
        "decision_id":
            snapshot.get("decision_id"),

        "intent_hash":
            snapshot.get("intent_hash"),

        "snapshot_hash":
            snapshot_hash,

        "outcome":
            snapshot.get("outcome"),

        "integrity_score":
            snapshot.get(
                "decision_integrity_score",
                0
            )
    }
