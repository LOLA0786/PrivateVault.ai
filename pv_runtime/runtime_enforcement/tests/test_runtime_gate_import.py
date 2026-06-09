import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pv_runtime.runtime_enforcement.runtime_gate import (
    authorize_execution
)

print("RUNTIME_GATE_IMPORTED")
print("PASS")
