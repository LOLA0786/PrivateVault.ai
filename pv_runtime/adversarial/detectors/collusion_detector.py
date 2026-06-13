from collections import Counter

class CollusionDetector:

    def score(self, agent_chain):

        if not agent_chain:
            return 0

        counts = Counter(agent_chain)

        duplicated = sum(
            c for c in counts.values()
            if c > 1
        )

        return min(
            duplicated * 15,
            100
        )
