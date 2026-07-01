"""
Canonical external request into the PrivateVault Decision Runtime.

Every agent framework submits ActionRequest.
The runtime derives every security artifact internally.
"""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

_EMPTY = MappingProxyType({})


@dataclass(frozen=True, slots=True)
class AgentIdentity:

    agent_id: str

    tenant_id: str = ""

    session_id: str = ""

    identity: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )


@dataclass(frozen=True, slots=True)
class LoopReference:

    loop_id: str = ""

    iteration: int = 0

    goal: str = ""

    max_iterations: int = 100


@dataclass(frozen=True, slots=True)
class DecisionGraphRef:

    graph_id: str = ""

    node_id: str = ""

    edge_id: str = ""

    policy_version: str = ""


@dataclass(frozen=True, slots=True)
class Proposal:

    intent: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )

    action: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )

    resources: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RuntimeLimits:

    max_cost_usd: float = 0.0

    max_iterations: int = 100

    max_latency_ms: int = 5000

    max_tokens: int = 0


@dataclass(frozen=True, slots=True)
class ActionRequest:
    """
    The ONLY public request object accepted by the runtime.
    """

    request_id: str

    agent: AgentIdentity

    proposal: Proposal

    loop: LoopReference = field(
        default_factory=LoopReference
    )

    graph: DecisionGraphRef = field(
        default_factory=DecisionGraphRef
    )

    context: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )

    limits: RuntimeLimits = field(
        default_factory=RuntimeLimits
    )

    previous_receipt: str = ""

    nonce: str = ""

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )
