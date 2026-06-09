#!/usr/bin/env bash
set -e

mkdir -p pv_runtime_v2/src/pv_runtime_v2
mkdir -p pv_runtime_v2/tests

mv pv_runtime_v2/trust_fabric pv_runtime_v2/src/pv_runtime_v2/
mv pv_runtime_v2/consensus pv_runtime_v2/src/pv_runtime_v2/
mv pv_runtime_v2/economics pv_runtime_v2/src/pv_runtime_v2/
mv pv_runtime_v2/runtime pv_runtime_v2/src/pv_runtime_v2/
mv pv_runtime_v2/evidence pv_runtime_v2/src/pv_runtime_v2/
mv pv_runtime_v2/benchmarks pv_runtime_v2/src/pv_runtime_v2/

touch pv_runtime_v2/src/pv_runtime_v2/__init__.py

echo "RESTRUCTURE COMPLETE"
