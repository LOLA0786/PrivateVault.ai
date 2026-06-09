class MemoryQuarantine:

    def __init__(self):
        self.quarantined = {}

    def quarantine(
        self,
        memory_id,
        reason
    ):
        self.quarantined[memory_id] = reason

    def restore(
        self,
        memory_id
    ):
        self.quarantined.pop(
            memory_id,
            None
        )

    def is_quarantined(
        self,
        memory_id
    ):
        return memory_id in self.quarantined
