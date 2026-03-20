#!/bin/bash
set -e

FILE="multi_agent_workflow.py"

# Import firewall
grep -q "firewall_check" $FILE || sed -i '1i from security.agent_firewall.firewall import firewall_check' $FILE

# Inject before tool/action execution (generic pattern)
grep -q "firewall_check(" $FILE || sed -i '/execute_action/a\    fw = firewall_check(action)\n    if fw["decision"] == "BLOCK":\n        print("🔥 Firewall blocked action:", action)\n        return fw\n    if fw["decision"] == "QUARANTINE":\n        print("⚠️ Firewall quarantined action:", action)\n        return fw' $FILE

