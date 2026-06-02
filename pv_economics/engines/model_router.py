class ModelRouter:

    ROUTES = {
        "simple":"gpt-5-mini",
        "standard":"gpt-5",
        "complex":"gpt-5-pro"
    }

    def recommend(
        self,
        complexity
    ):

        return self.ROUTES.get(
            complexity,
            "gpt-5"
        )
