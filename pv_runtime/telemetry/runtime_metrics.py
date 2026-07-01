"""
Canonical runtime telemetry.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeMetrics:

    latency_ms: float = 0.0

    input_tokens: int = 0
    output_tokens: int = 0
    used_tokens: int = 0

    total_tool_calls: int = 0
    useful_tool_calls: int = 0

    retries: int = 0
    rollbacks: int = 0

    cost_usd: float = 0.0
