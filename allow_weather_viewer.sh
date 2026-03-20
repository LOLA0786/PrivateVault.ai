#!/bin/bash
set -e

FILE="tool_authorization.py"

# Add weather_api to viewer allowed tools
sed -i 's/"viewer": {/"viewer": {"allowed_tools": ["weather_api"],/' $FILE

