#!/bin/bash
set -e

echo "[DEBUG] Inspecting execute_sim expectations"

python - << 'PYCODE'
import execute_sim
import inspect

# find runner
CANDIDATES = ["simulate_execution", "simulate_action", "run_simulation"]

runner = None
for name in CANDIDATES:
    if hasattr(execute_sim, name):
        runner = getattr(execute_sim, name)
        print(f"[FOUND] {name}")
        break

if runner:
    print("\n[SOURCE CODE]")
    print(inspect.getsource(runner))
else:
    print("No runner found")

# inspect profiles if exists
if hasattr(execute_sim, "profiles"):
    print("\n[PROFILES KEYS]")
    print(list(execute_sim.profiles.keys()))
PYCODE

echo "[DONE]"
