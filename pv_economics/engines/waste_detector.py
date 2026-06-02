class WasteDetector:

    def analyze(self, execution):

        retry_penalty = execution.retries * 5

        waste_score = min(retry_penalty, 100)

        return {
            "waste_score": waste_score,
            "retry_count": execution.retries
        }
