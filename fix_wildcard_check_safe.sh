#!/bin/bash
set -e

FILE="tool_authorization.py"

sed -i 's/tool_name in allowed_tools/"*" in allowed_tools or tool_name in allowed_tools/' $FILE

