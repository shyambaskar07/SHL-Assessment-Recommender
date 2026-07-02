import json


class Retriever:

    def __init__(self):

        with open(
            "data/catalog.json",
            "r",
            encoding="utf-8"
        ) as f:
            self.catalog = json.load(f)

    def retrieve(
        self,
        query,
        top_k=10
    ):

        query_words = set(
            query.lower().split()
        )

        scored = []

        for assessment in self.catalog:

            text = (
                (
                    assessment.get(
                        "name",
                        ""
                    )
                    + " "
                    + assessment.get(
                        "description",
                        ""
                    )
                    + " "
                    + " ".join(
                        assessment.get(
                            "keys",
                            []
                        )
                    )
                )
            ).lower()

            score = 0

            for word in query_words:
                if word in text:
                    score += 1

            if score > 0:
                scored.append(
                    (
                        score,
                        assessment
                    )
                )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, assessment in scored[
            :top_k
        ]:
            results.append(
                assessment
            )

        if len(results) == 0:
            results = self.catalog[:top_k]

        return results