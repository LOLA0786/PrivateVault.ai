#!/bin/bash
set -e

FILE="tool_authorization.py"

# remove all our injected patterns
sed -i '/admin_override/d' $FILE
sed -i '/SAFE_ADMIN_OVERRIDE/d' $FILE
sed -i '/FINAL_ADMIN_OVERRIDE/d' $FILE
sed -i '/ADMIN_SAFE_OVERRIDE/d' $FILE
sed -i '/ADMIN_OVERRIDE/d' $FILE
sed -i '/role = "admin"/d' $FILE
sed -i '/allowed_tools = \["\*"\]/d' $FILE

