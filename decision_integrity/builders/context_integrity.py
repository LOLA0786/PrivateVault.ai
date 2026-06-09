import hashlib


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def add_context(
    snapshot,
    content: str,
    source: str,
    trust_score: float,
):
    snapshot.context_hashes.append(
        sha256(content)
    )

    snapshot.context_sources.append(
        source
    )

    snapshot.context_trust_scores.append(
        trust_score
    )

    return snapshot


def context_integrity_score(snapshot):

    if not snapshot.context_trust_scores:
        return 100.0

    avg = (
        sum(snapshot.context_trust_scores)
        / len(snapshot.context_trust_scores)
    )

    return round(avg * 100, 2)
