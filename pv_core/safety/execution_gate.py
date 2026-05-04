import time
from typing import Dict, Any

_LAST_EXEC = {}

def allow_execution(action: Dict[str, Any], cooldown_sec: float = 2.0) -> bool:
    key = str(action.get("recipient") or action.get("idempotency_key") or "global")
    now = time.time()
    last = _LAST_EXEC.get(key)
    if last is not None and (now - last) < cooldown_sec:
        return False
    _LAST_EXEC[key] = now
    return True
