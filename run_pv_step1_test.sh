#!/bin/bash
set -e

echo "[TEST] Running Step 1 pipeline validation"

python - << 'PYCODE'
from pv_runtime.entrypoint import execute

result = execute(
    {"action": "health_check"},
    "agent_1"
)

print("[RESULT]")
print(result)
PYCODE

echo "[DONE] Step 1 test executed"
