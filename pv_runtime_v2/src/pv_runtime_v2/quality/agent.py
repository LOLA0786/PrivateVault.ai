from dataclasses import dataclass


@dataclass(slots=True)
class Agent:

    trust: float

    is_byzantine: bool = False
