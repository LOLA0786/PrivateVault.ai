"""
Decision Integrity Engine (DIE)
================================
Pre-execution decision correctness layer.

Sits between intent parsing and policy enforcement (PrivateVault firewall).
Validates structural soundness of a decision BEFORE it reaches ai_firewall_core.

Pipeline position:
    User Intent
        ↓
    Intent Parser
        ↓
    ⚡ DIE (this module)          ← you are here
        ↓
    ai_firewall_core.py           ← existing, untouched
        ↓
    policy_engine.py              ← existing, untouched
        ↓
    Execution

Public API (import from here, not from submodules):
    from die import DecisionObject, DIEResult, DecisionIntegrityEngine

Submodules:
    die.core.assumption_extractor  — surfaces implicit logic as explicit assumptions
    die.core.stress_tester         — simulates context variations
    die.core.stability_scorer      — scores decision fragility
    die.core.execution_gate        — emits PASS / RESTRICTED / BLOCKED

Author: PrivateVault team
Created: 2026-03
"""

from die.core.decision_object import DecisionObject
from die.core.execution_gate import DIEResult, ExecutionStatus
from die.core.engine import DecisionIntegrityEngine

__all__ = ["DecisionObject", "DIEResult", "ExecutionStatus", "DecisionIntegrityEngine"]
__version__ = "0.1.0"
