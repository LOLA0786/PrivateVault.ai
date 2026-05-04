import os
import random
from pv_cost_layer.router.learning import get_success_rate

WEIGHTS = {
    "cost": 0.3,
    "latency": 0.2,
    "success": 0.5,
}

MIN_SUCCESS = 0.85
EPSILON = float(os.getenv("PV_EPSILON", "0.2"))

PROFILES = {
    "gpt": {"cost": 0.012, "latency": 800, "success": 0.99},
    "grok": {"cost": 0.004, "latency": 900, "success": 0.80},
    "local": {"cost": 0.000, "latency": 300, "success": 0.70},
}


def _norm_cost(p):
    costs = [v["cost"] for v in PROFILES.values()]
    mn, mx = min(costs), max(costs)
    if mx == mn:
        return 1.0
    # lower cost -> higher score (0..1)
    return 1.0 - ((p["cost"] - mn) / (mx - mn))


def _norm_latency(p):
    lats = [v["latency"] for v in PROFILES.values()]
    mn, mx = min(lats), max(lats)
    if mx == mn:
        return 1.0
    # lower latency -> higher score (0..1)
    return 1.0 - ((p["latency"] - mn) / (mx - mn))


def score(provider: str) -> float:
    p = PROFILES[provider]
    success = get_success_rate(provider, p["success"])

    s_cost = _norm_cost(p)
    s_lat = _norm_latency(p)
    s_succ = success  # already 0..1

    return (
        WEIGHTS["cost"] * s_cost +
        WEIGHTS["latency"] * s_lat +
        WEIGHTS["success"] * s_succ
    )


def pick_best() -> str:
    providers = list(PROFILES.keys())

    # exploration
    if random.random() < EPSILON:
        return random.choice(providers)

    # quality gate with learned success
    valid = [
        p for p in providers
        if get_success_rate(p, PROFILES[p]["success"]) >= MIN_SUCCESS
    ]
    if not valid:
        valid = providers

    return max(valid, key=score)
