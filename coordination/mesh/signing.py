import hashlib
import hmac

SECRET_KEYS = {}

def register_key(agent_id, secret):
    SECRET_KEYS[agent_id] = secret

def sign_message(agent_id, message_hash):
    secret = SECRET_KEYS.get(agent_id)
    return hmac.new(
        secret.encode(),
        message_hash.encode(),
        hashlib.sha256
    ).hexdigest()

def verify_signature(agent_id, message_hash, signature):
    expected = sign_message(agent_id, message_hash)
    return expected == signature
