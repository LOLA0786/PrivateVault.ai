import json
import os
from collections import defaultdict
import math

STORE_PATH = "pv_cost_layer/router/learning_store.json"

STATS = defaultdict(lambda: {"success": 0, "total": 0})


def _load():
    global STATS
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, "r") as f:
            data = json.load(f)
            for k, v in data.items():
                STATS[k] = v


def _save():
    with open(STORE_PATH, "w") as f:
        json.dump(STATS, f)


_load()


def record(provider: str, success: bool):
    s = STATS[provider]
    s["total"] += 1
    if success:
        s["success"] += 1
    _save()


def get_success_rate(provider: str, default: float) -> float:
    s = STATS[provider]
    if s["total"] == 0:
        return default

    raw = s["success"] / s["total"]

    # confidence penalty (log scale)
    confidence = min(1.0, math.log(s["total"] + 1) / 5)

    return raw * confidence + default * (1 - confidence)
