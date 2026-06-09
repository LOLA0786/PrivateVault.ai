from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Vote:

    weight: float

    approve: bool


class WeightedQuorum:

    APPROVAL_THRESHOLD = 0.67

    def evaluate(
        self,
        votes: Iterable[Vote],
    ) -> float:

        total_weight = 0.0
        approval_weight = 0.0

        for vote in votes:

            total_weight += vote.weight

            if vote.approve:
                approval_weight += vote.weight

        if total_weight == 0:
            return 0.0

        return approval_weight / total_weight

    def approved(
        self,
        votes: Iterable[Vote],
    ) -> bool:

        return (
            self.evaluate(votes)
            >= self.APPROVAL_THRESHOLD
        )
