import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tool_authorization import authorize_tool_call

result = authorize_tool_call(
    "viewer_001",
    "file_system_read"
)

print("AUTHORIZED:", result["authorized"])
print("EXECUTED:", result["executed"])
print("PASS")
