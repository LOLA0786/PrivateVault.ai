#!/bin/bash
set -e

FILE="tool_authorization.py"

# remove ALL our injected override lines
sed -i '/SAFE_ADMIN_OVERRIDE/d' $FILE
sed -i '/admin_after_rbac/d' $FILE
sed -i '/if user_id == "admin"/d' $FILE

