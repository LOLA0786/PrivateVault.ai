import os

class FirewallConfig:
    # default = enterprise safe
    ENTERPRISE_MODE = os.getenv("PV_ENTERPRISE_MODE", "true").lower() == "true"

    # telemetry completely off in enterprise mode
    TELEMETRY_ENABLED = os.getenv("PV_TELEMETRY", "false").lower() == "true"

    # allow signal sharing only if explicitly enabled
    SIGNAL_SHARING = os.getenv("PV_SIGNAL_SHARING", "false").lower() == "true"

config = FirewallConfig()
