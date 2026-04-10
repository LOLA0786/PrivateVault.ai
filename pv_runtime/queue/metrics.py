class Metrics:
    def __init__(self):
        self.data = {
            "SUCCESS": 0,
            "FAILED": 0,
            "BLOCK": 0
        }

    def record(self, result):
        status = result.get("status")
        if status in self.data:
            self.data[status] += 1

    def report(self):
        return self.data
