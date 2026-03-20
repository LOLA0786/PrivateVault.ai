#!/bin/bash

set -e

FILE="execute_and_log.py"

grep -q "firewall_check" $FILE || sed -i "1i from security.agent_firewall.firewall import firewall_check" $FILE

grep -q "firewall_check(" $FILE || sed -i '/def execute/a\    fw = firewall_check(action)\n    if fw["decision"] == "BLOCK":\n        return {"status": "blocked", "fw": fw}\n    if fw["decision"] == "QUARANTINE":\n        return {"status": "quarantined", "fw": fw}' $FILE

