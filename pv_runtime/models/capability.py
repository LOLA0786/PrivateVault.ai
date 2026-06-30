"""
Canonical Capability model.

Represents a short-lived execution capability issued by the runtime.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Capability:
    """
    Immutable execution capability.
    """

    token: str

    capability_id: str = ""

    principal: str = ""

    action: str = ""

    issued_at: int = 0

    expires_at: int = 0

    single_use: bool = True
