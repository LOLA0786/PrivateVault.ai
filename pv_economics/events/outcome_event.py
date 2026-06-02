from new_features.execution_outcome.execution_outcome import (
    ExecutionOutcome
)


def build_outcome_event(
    success,
    business_result=None,
    metrics=None
):

    return ExecutionOutcome(
        success=success,
        business_result=business_result or {},
        metrics=metrics or {}
    )
