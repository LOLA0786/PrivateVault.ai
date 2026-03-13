from .evidence_record import EvidenceRecord
from .merkle_chain import MerkleChain


class EvidenceEngine:
    """
    Generates tamper-proof evidence for AI actions.
    """

    def __init__(self):
        self.merkle = MerkleChain()
        self.records = []

    def record(self, action, result):

        evidence = EvidenceRecord(action, result)

        evidence_hash = evidence.hash()

        merkle_root = self.merkle.add(evidence_hash)

        self.records.append({
            "hash": evidence_hash,
            "merkle_root": merkle_root,
            "record": evidence.to_dict()
        })

        return merkle_root
