#!/usr/bin/env python3

import subprocess
import sys

sys.exit(
    subprocess.call(
        ["python3", "tools/pv_verify.py"] + sys.argv[1:]
    )
)
