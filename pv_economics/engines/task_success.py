class TaskSuccessEngine:

    def evaluate(self, execution):

        return {
            "success": execution.success,
            "score": 100 if execution.success else 0
        }
