#!/bin/bash
set -e

echo "[DEBUG] Listing functions inside agent_identity.py"

python - << 'PYCODE'
import agent_identity

print("\n[AVAILABLE ATTRIBUTES]")
for attr in dir(agent_identity):
    if not attr.startswith("_"):
        obj = getattr(agent_identity, attr)
        if callable(obj):
            print("FUNC:", attr)
        else:
            print("VAR :", attr)
PYCODE

echo "[DONE] inspect output above"
