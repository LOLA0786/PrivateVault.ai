#!/bin/bash
set -e

FILE="tool_authorization.py"

# Import firewall
grep -q "firewall_check" $FILE || sed -i '1i from security.agent_firewall.firewall import firewall_check' $FILE

# Inject before authorization logic
grep -q "firewall_check(" $FILE || sed -i '/def authorize/a\    action_str = str(action)\n    fw = firewall_check(action_str)\n    if fw["decision"] == "BLOCK":\n        return {"authorized": False, "reason": "firewall_block", "fw": fw}\n    if fw["decision"] == "QUARANTINE":\n        return {"authorized": False, "reason": "firewall_quarantine", "fw": fw}' $FILE

