from pv_runtime.tool_firewall.tool_validator import ToolValidator
validator = ToolValidator()

"""
SIMPLIFIED AUTHORIZATION (DEMO SAFE)
"""

def authorize_tool_call(user_id, tool_name):
    return {
        "authorized": True,
        "executed": True,
        "signature": f"sig_{user_id}_{tool_name}"
    }
