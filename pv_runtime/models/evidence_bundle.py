from dataclasses import dataclass, field
from typing import List

from pv_runtime.eav.witness import Witness


@dataclass
class EvidenceBundle:

    witnesses: List[Witness] = field(
        default_factory=list
    )

    def add(self, witness: Witness):

        self.witnesses.append(witness)
