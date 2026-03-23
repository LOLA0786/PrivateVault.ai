from collections import deque
import time

WINDOW = deque(maxlen=20)

TIME_WINDOW = 60
HARD_LIMIT = 100000
SOFT_LIMIT = 70000
RATE_LIMIT = 2.5  # spike multiplier


def check(action):
    now = time.time()
    amount = action.get("amount", 0)

    WINDOW.append((now, amount))

    recent = [a for t, a in WINDOW if now - t < TIME_WINDOW]

    total = sum(recent)

    # 🚨 hard limit
    if total > HARD_LIMIT:
        return "BLOCK"

    # ⚠️ soft limit
    if total > SOFT_LIMIT:
        return "FLAG"

    # 🧠 spike detection (new)
    if len(recent) >= 2:
        if recent[-2] > 0 and (recent[-1] / recent[-2]) > RATE_LIMIT:
            return "BLOCK_SPIKE"

    return "OK"
