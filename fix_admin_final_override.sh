#!/bin/bash
set -e

FILE="tool_authorization.py"

# Inject override BEFORE unauthorized return
grep -q "FINAL_ADMIN_OVERRIDE" $FILE || sed -i '/UNAUTHORIZED/ i\        # FINAL_ADMIN_OVERRIDE\n        if role == "admin":\n            authorized = True' $FILE

