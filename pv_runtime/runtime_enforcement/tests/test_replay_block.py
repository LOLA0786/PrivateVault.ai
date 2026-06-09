import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from jwt_capability import (
    issue_jwt_cap,
    verify_jwt_cap
)

token = issue_jwt_cap(
    "decision-001",
    "process_payment",
    "agent_001"
)

print("FIRST_USE")

verify_jwt_cap(
    token,
    "process_payment",
    "agent_001"
)

print("FIRST_USE_OK")

try:

    verify_jwt_cap(
        token,
        "process_payment",
        "agent_001"
    )

    print("REPLAY_ALLOWED")

except Exception as e:

    print("REPLAY_BLOCKED")
    print(str(e))

print("PASS")
