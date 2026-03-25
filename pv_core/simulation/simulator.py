"""
SAFE WRAPPER - VALID PROVIDER MAPPING
"""

import inspect
import execute_sim

# detected runner
_runner = execute_sim.simulate_execution

# valid providers from source
VALID_PROVIDERS = ["gpt", "grok", "local"]


def run(intent):
    # normalize input safely
    provider = None

    if isinstance(intent, dict):
        provider = intent.get("provider") or intent.get("action")
    else:
        provider = intent

    # fallback if invalid
    if provider not in VALID_PROVIDERS:
        provider = "gpt"

    return _runner(provider)


if __name__ == "__main__":
    print("[CHECK] simulator loaded")
    print("[CHECK] using simulate_execution")
    print(inspect.getsource(_runner))
