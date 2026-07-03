from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class CanonicalEnterpriseAction:

    actor: Optional[str] = None

    verb: Optional[str] = None

    object_id: Optional[str] = None

    object_type: Optional[str] = None

    amount: Optional[float] = None

    currency: Optional[str] = None

    purpose: Optional[str] = None

    constraints: Dict[str, Any] = field(default_factory=dict)
