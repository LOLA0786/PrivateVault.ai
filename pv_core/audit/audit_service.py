"""
SAFE WRAPPER - AUDIT WITH EXTERNAL PATH FIX
"""

import inspect
import os
from audit_logger import log_audit_event

# FIX: must be outside repo
DEFAULT_AUDIT_PATH = "/tmp/privatevault_audit.log"

if "PV_AUDIT_LOG_PATH" not in os.environ:
    os.environ["PV_AUDIT_LOG_PATH"] = DEFAULT_AUDIT_PATH


def log(payload):
    return log_audit_event(payload)


if __name__ == "__main__":
    print("[CHECK] audit_service loaded")
    print("[CHECK] using log_audit_event")
    print(inspect.getsource(log_audit_event))
