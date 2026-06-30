"""
Canonical RuntimeContext model.

Every privileged execution inside PrivateVault should eventually flow
through this immutable object.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping
from types import MappingProxyType

from pv_runtime.models.approval import Approval
from pv_runtime.models.capability import Capability
from pv_runtime.models.decision import Decision


_EMPTY = MappingProxyType({})


@dataclass(frozen=True, slots=True)
class RuntimeContext:
    """
    Immutable execution context.
    """

    agent_id: str

    identity: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)
    tenant: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)

    intent: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)
    context: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)

    simulation: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)
    risk: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)

    decision: Decision | None = None
    approval: Approval | None = None
    capability: Capability | None = None

    runtime_security: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)

    execution: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)

    evidence: Mapping[str, Any] = field(default_factory=lambda: _EMPTY)
