import time

class RetryEngine:

    def execute_with_retry(self, func, retries=3, delay=1):
        for i in range(retries):
            try:
                return func()
            except Exception:
                time.sleep(delay)

        return {"status": "FAILED"}
