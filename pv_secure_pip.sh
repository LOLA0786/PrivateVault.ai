#!/bin/bash

echo "[PV] Secure pip install sandbox"

# isolate HOME (no access to real creds)
export HOME=/tmp/pv_home
mkdir -p $HOME

# wipe sensitive env
unset AWS_SECRET_ACCESS_KEY
unset AWS_ACCESS_KEY_ID
unset OPENAI_API_KEY
unset GOOGLE_API_KEY

# block network via pip (best-effort)
PIP_NO_CACHE_DIR=off pip install "$@"
