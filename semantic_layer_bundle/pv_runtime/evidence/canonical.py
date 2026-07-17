import hashlib
import json


def canonical_for_signature(receipt: dict) -> bytes:
    r = dict(receipt)
    r.pop("signature", None)
    r.pop("receipt_hash", None)
    r.pop("previous_receipt_hash", None)

    return json.dumps(
        r,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode()


def canonical_for_chain(receipt: dict) -> bytes:
    r = dict(receipt)
    r.pop("receipt_hash", None)

    return json.dumps(
        r,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode()


def compute_signature_hash(receipt: dict):
    return hashlib.sha256(
        canonical_for_signature(receipt)
    ).hexdigest()


def compute_chain_hash(receipt: dict):
    return hashlib.sha256(
        canonical_for_chain(receipt)
    ).hexdigest()
