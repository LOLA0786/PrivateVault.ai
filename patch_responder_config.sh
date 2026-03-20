#!/bin/bash
set -e

FILE="security/agent_firewall/responder.py"

grep -q "FirewallConfig" $FILE || sed -i '1i from .config import config' $FILE

# add safe telemetry guard
grep -q "TELEMETRY_ENABLED" $FILE || sed -i '/log_event(event)/a\    if not config.TELEMETRY_ENABLED:\n        return' $FILE

