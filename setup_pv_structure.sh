#!/bin/bash
set -e

echo "[+] Creating clean architecture (non-destructive)"

mkdir -p pv_core/{intent,policy,risk,simulation,enforcement,identity}
mkdir -p pv_control_plane
mkdir -p pv_connectors
mkdir -p pv_runtime
mkdir -p pv_observability
mkdir -p pv_enterprise
mkdir -p legacy
mkdir -p scripts/patches
mkdir -p docs/architecture

echo "[✓] Structure created safely"
