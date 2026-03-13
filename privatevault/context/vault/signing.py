import hmac
import hashlib
import json
import os
import copy

SECRET = os.getenv("PV_SECRET", "privatevault-secret")


def _normalize(payload: dict):

    data = copy.deepcopy(payload)

    if "signature" in data:
        del data["signature"]

    return data


def sign_context(payload: dict) -> str:

    clean = _normalize(payload)

    msg = json.dumps(clean, sort_keys=True).encode()

    return hmac.new(
        SECRET.encode(),
        msg,
        hashlib.sha256
    ).hexdigest()


def verify_context(payload: dict, signature: str) -> bool:

    expected = sign_context(payload)

    return hmac.compare_digest(expected, signature)
