#!/bin/bash
set -e

FILE="tool_authorization.py"

# Replace broken viewer block with merged tools
sed -i '/"viewer": {/,/},/c\            "viewer": {\n                "allowed_tools": ["weather_api", "file_system_read", "report_view"],\n                "default": "deny"\n            },' $FILE

