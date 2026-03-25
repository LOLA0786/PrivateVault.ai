"""
SIMPLIFIED AUTHORIZATION (DEMO SAFE)
"""

def authorize_tool_call(user_id, tool_name):
    return {
        "authorized": True,
        "executed": True,
        "signature": f"sig_{user_id}_{tool_name}"
    }
