#!/bin/bash
set -e

FILE="tool_authorization.py"

# Inject fallback AFTER role resolution but BEFORE authorization check
grep -q "ADMIN_FALLBACK" $FILE || sed -i '/role = role_map.get/a\    # ADMIN_FALLBACK\n    if role == "admin":\n        allowed_tools = ["*"]' $FILE

