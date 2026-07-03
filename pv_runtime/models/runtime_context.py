from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from pv_runtime.models.evidence_bundle import (
    EvidenceBundle,
)


@dataclass
class RuntimeContext:

    principal: Optional[str] = None

    action: Optional[str] = None

    declared_intent: Optional[Dict[str, Any]] = None

    executed_intent: Optional[Dict[str, Any]] = None

    approval: Optional[Dict[str, Any]] = None

    capability_token: Optional[str] = None

    evidence: EvidenceBundle = field(
        default_factory=EvidenceBundle
    )
