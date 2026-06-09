import hashlib


class EvidenceChain:

    @staticmethod
    def hash_event(
        previous_hash: str,
        payload: str,
    ) -> str:

        digest = hashlib.sha256()

        digest.update(
            previous_hash.encode()
        )

        digest.update(
            payload.encode()
        )

        return digest.hexdigest()
