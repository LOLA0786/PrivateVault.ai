#!/bin/bash
set -e

FILE="tool_authorization.py"

# Insert role mapping near top if not exists
grep -q "USER_ROLE_MAP" $FILE || sed -i '1i USER_ROLE_MAP = {"admin": "admin", "user1": "viewer", "user2": "viewer", "user3": "viewer"}' $FILE

# Replace role assignment
sed -i 's/user_role = .*/user_role = USER_ROLE_MAP.get(user_id, "viewer")/' $FILE

