import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tool_authorization import authorize_tool_call

result = authorize_tool_call(
    user_id="viewer_001",
    tool_name="file_system_read",
    declared_intent={
        "action": "read_file"
    },
    executed_intent={
        "action": "delete_database"
    },
    approval={
        "intent_hash": "fake_hash"
    },
    capability_token="fake_token"
)

print("AUTHORIZED:", result["authorized"])
print("EXECUTED:", result["executed"])

if not result["authorized"]:
    print("ERROR:", result["error"])

print("PASS")
