import json
import hashlib

def bind_intent(action):
    try:
        payload = json.dumps(action, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()
    except Exception:
        return None
