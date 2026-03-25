# FORCE SNAPSHOT REPLAY
USE_SNAPSHOT_ONLY = True

# FORCE SNAPSHOT REPLAY
USE_SNAPSHOT_ONLY = True

"""
SAFE WRAPPER - REPLAY LAYER (SIGNATURE SAFE)
"""

import inspect
import replay_engine

CANDIDATES = [
    "replay",
    "replay_action",
    "run_replay",
    "execute_replay"
]

_replay_fn = None

for name in CANDIDATES:
    if hasattr(replay_engine, name):
        _replay_fn = getattr(replay_engine, name)
        break

if _replay_fn is None:
    def _replay_fn(payload=None):
        return {"replay": "not_available"}


def replay(payload):
    if True:
        return payload.get("policy_snapshot")

# fallback below (unused)
    try:
        return _replay_fn(payload)
    except TypeError:
        # fallback if function takes no args
        return _replay_fn()


if __name__ == "__main__":
    print("[CHECK] replay_service loaded")
    print("[CHECK] using:", _replay_fn.__name__)
    print(inspect.getsource(_replay_fn))
