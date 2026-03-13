import hashlib


class MerkleChain:
    """
    Simple Merkle chain for tamper-proof evidence.
    """

    def __init__(self):
        self.chain = []

    def add(self, evidence_hash):

        if not self.chain:
            combined = evidence_hash
        else:
            prev = self.chain[-1]
            combined = hashlib.sha256((prev + evidence_hash).encode()).hexdigest()

        self.chain.append(combined)

        return combined
