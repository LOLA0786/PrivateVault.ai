#!/bin/bash
set -e

FILE="security/agent_firewall/anomaly.py"

sed -i 's/return 0.8/return 0.4/' $FILE
sed -i 's/return 0.1/return 0.05/' $FILE

