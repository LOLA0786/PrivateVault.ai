#!/bin/bash
set -e

echo "[DEBUG] Listing functions inside tool_authorization.py"

python - << 'PYCODE'
import tool_authorization

print("\n[AVAILABLE ATTRIBUTES]")
for attr in dir(tool_authorization):
    if not attr.startswith("_"):
        obj = getattr(tool_authorization, attr)
        if callable(obj):
            print("FUNC:", attr)
        else:
            print("VAR :", attr)
PYCODE

echo "[DONE]"
