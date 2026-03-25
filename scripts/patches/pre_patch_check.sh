#!/bin/bash

set -e

echo "[STEP] Running safety checks before any patch..."

echo "\n[CHECK] policy usage"
grep -R "evaluate_policy" . || true

echo "\n[CHECK] simulation usage"
grep -R "simulate_action" . || true

echo "\n[CHECK] identity usage"
grep -R "get_agent_identity" . || true

echo "\n[CHECK] duplicate wrappers (should be ONLY in pv_core)"
grep -R "pv_core" . || true

echo "\n[MANUAL ACTION REQUIRED]"
echo "1. Ensure no duplicate implementations exist"
echo "2. Ensure wrappers point to correct legacy functions"
echo "3. DO NOT PROCEED if conflicts found"

echo "[DONE] pre_patch_check completed"
