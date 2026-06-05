"""
Outcome Event — lightweight builder for execution outcome dicts.
No external imports — fully self-contained.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ExecutionOutcome:
    success:        bool
    business_result: Dict[str, Any] = field(default_factory=dict)
    metrics:        Dict[str, Any]  = field(default_factory=dict)
    partial:        bool            = False
    error_code:     Optional[str]   = None
    error_severity: str             = "medium"


def build_outcome_event(
    success:         bool,
    business_result: Optional[Dict] = None,
    metrics:         Optional[Dict] = None,
    partial:         bool           = False,
    error_code:      Optional[str]  = None,
    error_severity:  str            = "medium",
) -> ExecutionOutcome:

    return ExecutionOutcome(
        success=success,
        business_result=business_result or {},
        metrics=metrics or {},
        partial=partial,
        error_code=error_code,
        error_severity=error_severity,
    )
