#!/bin/bash
set -e

echo "[DEBUG] Listing functions inside policy_engine.py"

python - << 'PYCODE'
import policy_engine

print("\n[AVAILABLE ATTRIBUTES]")
for attr in dir(policy_engine):
    if not attr.startswith("_"):
        obj = getattr(policy_engine, attr)
        if callable(obj):
            print("FUNC:", attr)
        else:
            print("VAR :", attr)
PYCODE

echo "[DONE] inspect output above"
