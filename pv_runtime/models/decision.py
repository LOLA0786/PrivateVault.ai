"""
Canonical Decision model.

This immutable model represents the result of policy evaluation.

It is the only decision object that should cross runtime boundaries.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True, slots=True)
class Decision:
    """
    Immutable authorization decision.
    """

    allowed: bool
    reason: str = ""

    risk_score: float = 0.0

    policy_version: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)
