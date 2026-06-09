import jwt
import time
import uuid
import redis

SECRET = "283ddef35a96af2c756690e2aab666f4c6ab83d824d8d9bea8c5ac8243764e7d"
TTL = 300

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def is_blacklisted(jti):
    return False


def record_replay_attempt(principal):
    print(f"REPLAY_ATTEMPT:{principal}")


def issue_jwt_cap(
    decision_id,
    action,
    principal
):
    jti = str(uuid.uuid4())

    payload = {
        "jti": jti,
        "decision_id": decision_id,
        "action": action,
        "principal": principal,
        "exp": time.time() + TTL,
    }

    return jwt.encode(
        payload,
        SECRET,
        algorithm="HS256"
    )


def verify_jwt_cap(
    token,
    action,
    principal
):
    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

    except Exception:
        raise Exception(
            "INVALID_CAPABILITY_TOKEN"
        )

    jti = payload["jti"]

    if is_blacklisted(jti):
        raise Exception(
            "TOKEN_BLACKLISTED"
        )

    if payload["action"] != action:
        raise Exception(
            "ACTION_MISMATCH"
        )

    if payload["principal"] != principal:
        raise Exception(
            "PRINCIPAL_MISMATCH"
        )

    key = f"used_jti:{jti}"

    if r.exists(key):
        record_replay_attempt(
            principal
        )

        raise Exception(
            "REPLAY_DETECTED"
        )

    ttl = int(
        payload["exp"] - time.time()
    )

    r.setex(
        key,
        max(ttl, 1),
        "1"
    )

    return payload
