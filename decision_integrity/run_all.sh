#!/bin/bash

set -e

python3 decision_integrity/tests/test_snapshot_builder.py

python3 decision_integrity/tests/test_integrity_score.py

python3 decision_integrity/tests/test_context_integrity.py

python3 decision_integrity/tests/test_context_security.py

python3 decision_integrity/tests/test_decision_authorization.py

python3 decision_integrity/tests/test_decision_contract.py

python3 decision_integrity/demo_decision_security_control_plane.py

echo
echo "===================================="
echo "DECISION SECURITY CONTROL PLANE OK"
echo "===================================="
