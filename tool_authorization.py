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

# === CLOSED-LOOP INTEGRATION POINT (additive) ===
from new_features.execution_outcome.closed_loop_wrapper import fire_closed_loop
# Usage (1 line after tool execution):
# fire_closed_loop(intent_hash, outcome_dict)

# === ENTERPRISE CLOSED-LOOP INTEGRATION (additive only) ===

from new_features.execution_outcome.enterprise import fire_closed_loop

# After tool execution: fire_closed_loop(intent_hash, outcome_data)

