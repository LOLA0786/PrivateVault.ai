#!/bin/bash
set -e

FILE="security/agent_firewall/classifier.py"

# Add import
grep -q "baseline" $FILE || sed -i '1i from .baseline import is_safe_action' $FILE

# Replace classify function
cat <<'PYEOF' > /tmp/new_classifier.py
from .anomaly import anomaly_score
from .baseline import is_safe_action

def classify(flags, action):
    if not flags:
        base = "LOW"
    elif any(f["severity"] == "HIGH" for f in flags):
        base = "HIGH"
    elif any(f["severity"] == "MEDIUM" for f in flags):
        base = "MEDIUM"
    else:
        base = "LOW"

    # Safe actions should not escalate easily
    if is_safe_action(action) and base == "LOW":
        return "LOW"

    anomaly = anomaly_score(action)

    # Only escalate if anomaly is high AND there is some signal
    if anomaly > 0.6 and base == "MEDIUM":
        return "MEDIUM"

    return base
PYEOF

# Replace function
sed -i '/def classify/,/return base/d' $FILE
cat /tmp/new_classifier.py >> $FILE

