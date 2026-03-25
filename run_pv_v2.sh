#!/bin/bash

echo "[+] Running new structured pipeline"

python -c "
from pv_runtime.entrypoint import execute

print(execute(
    {'action':'test'},
    'agent_1'
))
"
