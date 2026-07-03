import hashlib
import json
import os

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

KEY_ENV = "PV_RECEIPT_SIGNING_KEY"


def _key():

    key = os.getenv(KEY_ENV)

    if not key:
        raise RuntimeError(
            f"{KEY_ENV} not set"
        )

    return SigningKey(
        key,
        encoder=HexEncoder,
    )


def public_key():

    return (
        _key()
        .verify_key
        .encode(
            encoder=HexEncoder,
        )
        .decode()
    )


def sign_receipt(receipt):

    canonical = json.dumps(
        receipt,
        sort_keys=True,
        default=str,
    )

    digest = hashlib.sha256(
        canonical.encode()
    ).hexdigest()

    signature = (
        _key()
        .sign(
            digest.encode()
        )
        .signature
        .hex()
    )

    return {
        "algorithm": "Ed25519",
        "receipt_hash": digest,
        "signature": signature,
        "public_key": public_key(),
    }



def verify_receipt(receipt):

    r = dict(receipt)

    sig = r.pop("signature")

    r.pop("receipt_hash", None)
    r.pop("previous_receipt_hash", None)

    canonical = json.dumps(
        r,
        sort_keys=True,
        default=str,
    )

    digest = hashlib.sha256(
        canonical.encode()
    ).hexdigest()

    if digest != sig["receipt_hash"]:
        return False

    try:
        VerifyKey(
            sig["public_key"],
            encoder=HexEncoder,
        ).verify(
            digest.encode(),
            bytes.fromhex(sig["signature"]),
        )
        return True
    except BadSignatureError:
        return False
