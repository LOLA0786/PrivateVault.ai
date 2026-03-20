#!/bin/bash
set -e

FILE="tool_authorization.py"

sed -i '/CLEAN_ADMIN_OVERRIDE/d' $FILE
sed -i '/admin_override/d' $FILE

