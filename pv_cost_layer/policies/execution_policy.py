from pv_cost_layer.router.learning import get_success_rate
from pv_cost_layer.router.scoring import PROFILES

MIN_SUCCESS = 0.85


def evaluate_providers():
    allowed = []
    rejected = {}

    for p, prof in PROFILES.items():
        s = get_success_rate(p, prof["success"])

        if s >= MIN_SUCCESS:
            allowed.append(p)
        else:
            rejected[p] = {
                "reason": "low_success_rate",
                "value": s,
                "threshold": MIN_SUCCESS
            }

    if not allowed:
        allowed = list(PROFILES.keys())

    return allowed, rejected
