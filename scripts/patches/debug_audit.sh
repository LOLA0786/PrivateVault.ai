#!/bin/bash
set -e

echo "[DEBUG] Listing functions inside audit_logger.py"

python - << 'PYCODE'
import audit_logger

print("\n[AVAILABLE ATTRIBUTES]")
for attr in dir(audit_logger):
    if not attr.startswith("_"):
        obj = getattr(audit_logger, attr)
        if callable(obj):
            print("FUNC:", attr)
        else:
            print("VAR :", attr)
PYCODE

echo "[DONE]"
