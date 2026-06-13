class ConfusableDetector:

    CYRILLIC_CHARS = set(
        "АВСЕНКМОРТХаеорсху"
    )

    def score(self, text=""):

        if not text:
            return 0

        hits = 0

        for ch in text:
            if ch in self.CYRILLIC_CHARS:
                hits += 1

        if hits == 0:
            return 0

        return min(hits * 10, 40)
