#!/bin/bash
set -e

FILE="tool_authorization.py"

# Remove bad injected line
sed -i '/allowed_tools = \["\*"\]/d' $FILE

