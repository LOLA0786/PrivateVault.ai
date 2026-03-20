#!/bin/bash
set -e

FILE="tool_authorization.py"

# Add import if missing
grep -q "from datetime import timezone" $FILE || sed -i '1i from datetime import timezone' $FILE

