import hashlib
import json
import os

from nacl.encoding import HexEncoder
from nacl.signing import SigningKey

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
        "receipt_hash": digest,
        "signature": signature,
        "public_key": public_key(),
    }
