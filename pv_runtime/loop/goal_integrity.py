"""
Goal Integrity.

Ensures the loop objective never silently changes.
"""

import hashlib


def goal_hash(goal: str) -> str:
    return hashlib.sha256(
        goal.encode()
    ).hexdigest()


def verify_goal(original_hash, current_goal):

    if goal_hash(current_goal) != original_hash:
        raise Exception("GOAL_MUTATION_DETECTED")

    return True
