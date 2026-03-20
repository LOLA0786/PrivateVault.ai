#!/bin/bash
set -e

FILE="tool_authorization.py"

sed -i '/ADMIN_OVERRIDE/d' $FILE
sed -i '/ADMIN_SAFE_OVERRIDE/d' $FILE
sed -i '/FINAL_ADMIN_OVERRIDE/d' $FILE

