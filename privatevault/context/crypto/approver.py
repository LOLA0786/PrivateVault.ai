import hmac
import hashlib
import os

KEYS = {
    "CRO": os.getenv("CRO_KEY", "cro-secret"),
    "LEGAL": os.getenv("LEGAL_KEY", "legal-secret")
}


def sign(role: str, payload: str) -> str:

    key = KEYS.get(role)

    if not key:
        raise Exception("Unknown role")

    return hmac.new(
        key.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()


def verify(role: str, payload: str, sig: str) -> bool:

    expected = sign(role, payload)

    return hmac.compare_digest(expected, sig)
