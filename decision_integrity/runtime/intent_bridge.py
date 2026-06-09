import hashlib
import json


def canonical_intent_hash(intent):

    payload = json.dumps(
        intent,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        payload.encode()
    ).hexdigest()
