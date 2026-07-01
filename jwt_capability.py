import jwt
import time
import uuid
import os

from pv_runtime.security.replay_provider import (
    get_replay_store,
)

SECRET = os.getenv(
    "PV_CAPABILITY_SECRET"
)

if SECRET is None:
    raise RuntimeError(
        "PV_CAPABILITY_SECRET is required."
    )

if len(SECRET.encode("utf-8")) < 32:
    raise RuntimeError(
        "PV_CAPABILITY_SECRET must be at least 32 bytes."
    )

TTL = 300


def is_blacklisted(jti):
    return False


def record_replay_attempt(principal):
    print(f"REPLAY_ATTEMPT:{principal}")


def issue_jwt_cap(
    decision_id,
    action,
    principal,
):

    payload = {
        "jti": str(uuid.uuid4()),
        "decision_id": decision_id,
        "action": action,
        "principal": principal,
        "exp": time.time() + TTL,
    }

    return jwt.encode(
        payload,
        SECRET,
        algorithm="HS256",
    )


def verify_jwt_cap(
    token,
    action,
    principal,
):

    try:

        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
        )

    except Exception:

        raise Exception(
            "INVALID_CAPABILITY_TOKEN"
        )

    if payload["action"] != action:
        raise Exception("ACTION_MISMATCH")

    if payload["principal"] != principal:
        raise Exception("PRINCIPAL_MISMATCH")

    jti = payload["jti"]

    if is_blacklisted(jti):
        raise Exception("TOKEN_BLACKLISTED")

    replay = get_replay_store()

    key = f"used_jti:{jti}"

    if replay.exists(key):

        record_replay_attempt(
            principal,
        )

        raise Exception(
            "REPLAY_DETECTED"
        )

    ttl = int(
        payload["exp"] - time.time()
    )

    replay.put(
        key,
        max(ttl, 1),
    )

    return payload
