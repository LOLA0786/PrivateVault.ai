"""
Canonical response returned by the PrivateVault Decision Runtime.
"""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

_EMPTY = MappingProxyType({})


@dataclass(frozen=True, slots=True)
class DecisionResult:
    """
    Runtime policy decision.
    """

    allowed: bool

    reason: str

    policy_version: str = ""

    risk_score: float = 0.0


@dataclass(frozen=True, slots=True)
class CapabilityGrant:
    """
    Capability issued by the runtime.
    """

    capability_id: str = ""

    token: str = ""

    expires_at: int = 0


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """
    Execution summary.
    """

    executed: bool

    status: str

    result: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )


@dataclass(frozen=True, slots=True)
class ReceiptReference:
    """
    Cryptographic proof.
    """

    receipt_hash: str = ""

    merkle_root: str = ""

    previous_hash: str = ""


@dataclass(frozen=True, slots=True)
class ActionResponse:
    """
    Canonical runtime response.
    """

    request_id: str

    decision: DecisionResult

    execution: ExecutionResult

    capability: CapabilityGrant = field(
        default_factory=CapabilityGrant
    )

    receipt: ReceiptReference = field(
        default_factory=ReceiptReference
    )

    metrics: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )

    metadata: Mapping[str, Any] = field(
        default_factory=lambda: _EMPTY
    )
