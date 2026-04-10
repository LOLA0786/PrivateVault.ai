import time
import random

class RetryEngine:

    def execute_with_retry(self, func, retries=5):
        for attempt in range(retries):
            result = func()

            if result.get("status") != "LOCKED":
                return result

            # exponential backoff with jitter
            time.sleep(0.01 * (2 ** attempt) + random.random() * 0.01)

        return {"status": "FAILED", "reason": "Max retries exceeded"}
