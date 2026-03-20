#!/bin/bash
set -e

FILE="tool_authorization.py"

sed -i 's/action_str = str(params)/action_str = str(params.get("action",""))/' $FILE

