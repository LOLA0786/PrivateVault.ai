#!/bin/bash

set -e

echo "=================================="
echo "PrivateVault PII Runtime Validation"
echo "=================================="

python test_pii.py
python test_pii_evidence.py
python test_pii_enterprise.py
python test_pii_deny_enterprise.py
python verify_pii_runtime.py

echo
echo "ALL TESTS PASSED"
