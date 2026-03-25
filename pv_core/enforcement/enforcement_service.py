"""
SAFE WRAPPER - INPUT NORMALIZATION FOR authorize_tool_call
"""

import inspect
from tool_authorization import authorize_tool_call


def enforce(intent, decision):
    # FIX: function expects user_id (string), not full dict
    if isinstance(intent, dict):
        user_id = intent.get("agent_id") or intent.get("user_id") or "default_user"
    else:
        user_id = intent

    return authorize_tool_call(user_id, decision)


if __name__ == "__main__":
    print("[CHECK] enforcement_service loaded")
    print("[CHECK] using authorize_tool_call")
    print(inspect.getsource(authorize_tool_call))
