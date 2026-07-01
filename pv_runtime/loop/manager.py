"""
Loop Manager.

Owns the lifecycle of immutable LoopContext objects.

This module performs NO execution.
"""

from dataclasses import replace
from uuid import uuid4

from pv_runtime.loop.models import LoopContext


class LoopManager:
    """
    Canonical loop lifecycle manager.
    """

    def start(
        self,
        *,
        goal: str,
        runtime_context,
        max_iterations: int = 100,
    ) -> LoopContext:

        return LoopContext(
            loop_id=str(uuid4()),
            goal=goal,
            iteration=0,
            max_iterations=max_iterations,
            runtime_context=runtime_context,
        )

    def next_iteration(
        self,
        loop: LoopContext,
        runtime_context,
    ) -> LoopContext:

        return replace(
            loop,
            iteration=loop.iteration + 1,
            runtime_context=runtime_context,
        )

    def finished(
        self,
        loop: LoopContext,
    ) -> bool:

        return loop.iteration >= loop.max_iterations
