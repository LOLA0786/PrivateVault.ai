#!/bin/bash
set -e

FILE="tool_authorization.py"

# Replace wrong variable
sed -i 's/action_str = str(action)/action_str = str(params)/' $FILE

