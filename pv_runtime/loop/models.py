"""
Canonical Loop runtime models.

Every autonomous loop is represented by an immutable LoopContext.
"""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from pv_runtime.models.runtime_context import RuntimeContext

_EMPTY = MappingProxyType({})


@dataclass(frozen=True, slots=True)
class LoopEconomics:
    """
    Economics accumulated across the loop.
    """

    total_cost: float = 0.0
    token_cost: float = 0.0
    tool_cost: float = 0.0

    latency_ms: float = 0.0

    input_tokens: int = 0
    output_tokens: int = 0
    used_tokens: int = 0

    total_tool_calls: int = 0
    useful_tool_calls: int = 0

    context_bytes: int = 0
    referenced_bytes: int = 0
    wasted_bytes: int = 0

    retries: int = 0
    rollbacks: int = 0


@dataclass(frozen=True, slots=True)
class LoopHealth:
    """
    Runtime health of the loop.
    """

    score: float = 100.0

    converging: bool = True

    drift_detected: bool = False

    stop_reason: str = ""


@dataclass(frozen=True, slots=True)
class LoopEvidence:
    """
    Cryptographic evidence for the loop.
    """

    previous_hash: str = ""

    current_hash: str = ""

    merkle_root: str = ""


@dataclass(frozen=True, slots=True)
class LoopContext:
    """
    Canonical runtime loop object.
    """

    loop_id: str

    goal: str

    iteration: int

    max_iterations: int

    runtime_context: RuntimeContext

    economics: LoopEconomics = field(
        default_factory=LoopEconomics
    )

    health: LoopHealth = field(
        default_factory=LoopHealth
    )

    evidence: LoopEvidence = field(
        default_factory=LoopEvidence
    )

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )
