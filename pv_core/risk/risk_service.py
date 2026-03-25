"""
SAFE WRAPPER - RISK (AUTO-DETECT)
"""

import inspect
import drift_detection

CANDIDATES = [
    "detect_drift",
    "calculate_risk",
    "infer_risk",
    "risk_score"
]

_risk_fn = None

for name in CANDIDATES:
    if hasattr(drift_detection, name):
        _risk_fn = getattr(drift_detection, name)
        break

# fallback to policy_engine if needed
if _risk_fn is None:
    import policy_engine
    if hasattr(policy_engine, "infer_risk"):
        _risk_fn = getattr(policy_engine, "infer_risk")

if _risk_fn is None:
    raise ImportError("No risk function found")


def score(intent, simulation):
    return _risk_fn(intent, simulation)


if __name__ == "__main__":
    print("[CHECK] risk_service loaded")
    print("[CHECK] using:", _risk_fn.__name__)
    print(inspect.getsource(_risk_fn))
