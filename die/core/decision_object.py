"""
die.core.decision_object
========================
Formal contract for a decision entering the DIE pipeline.

Every agent action MUST be expressed as a DecisionObject before
it can be validated. This is the input schema for DIE.

Fields
------
action      : what the agent wants to do  (e.g. "offer_discount")
goal        : why it wants to do it       (e.g. "increase_conversion")
context     : runtime facts               (e.g. user_type, cart_value)
constraints : hard limits that must hold  (e.g. max_discount, margin_floor)

Usage
-----
    from die import DecisionObject

    d = DecisionObject(
        action="offer_discount",
        goal="increase_conversion",
        context={"user_type": "new_customer", "cart_value": 120},
        constraints={"max_discount": 20, "margin_floor": 15},
    )
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DecisionObject:
    """Immutable contract describing a single agent decision."""

    action:      str
    goal:        str
    context:     dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        """
        Returns a list of validation errors.
        Empty list means the object is structurally complete.
        """
        errors = []
        if not self.action.strip():
            errors.append("action must not be empty")
        if not self.goal.strip():
            errors.append("goal must not be empty")
        if not isinstance(self.context, dict):
            errors.append("context must be a dict")
        if not isinstance(self.constraints, dict):
            errors.append("constraints must be a dict")
        return errors

    def to_dict(self) -> dict:
        return {
            "action":      self.action,
            "goal":        self.goal,
            "context":     self.context,
            "constraints": self.constraints,
        }
