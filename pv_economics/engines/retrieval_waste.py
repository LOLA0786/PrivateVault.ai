class RetrievalWaste:

    def analyze(
        self,
        retrieved_docs,
        cited_docs
    ):

        wasted = max(
            retrieved_docs - cited_docs,
            0
        )

        return {
            "wasted_docs": wasted,
            "waste_percent":
                round(
                    wasted /
                    max(retrieved_docs, 1)
                    * 100,
                    2
                )
        }
