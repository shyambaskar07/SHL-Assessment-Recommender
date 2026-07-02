from app.services.retriever import Retriever
from app.services.ranker import Ranker


class Recommender:

    def __init__(self):
        self.retriever = Retriever()
        self.ranker = Ranker()

    def recommend(
        self,
        state,
        top_k=10
    ):

        query_parts = []

        if state.role:
            query_parts.append(
                state.role
            )

        if state.seniority:
            query_parts.append(
                state.seniority
            )

        if state.technical_required:
            query_parts.append(
                "technical assessment"
            )

        if state.communication_required:
            query_parts.append(
                "communication skills"
            )

        if state.personality_required:
            query_parts.append(
                "personality assessment"
            )

        if state.leadership_required:
            query_parts.append(
                "leadership assessment"
            )

        query = " ".join(
            query_parts
        )

        candidates = self.retriever.retrieve(
            query=query,
            top_k=30
        )

        scored = []

        for item in candidates:

            score = self.ranker.score(
                item,
                state
            )

            scored.append(
                (
                    score,
                    item
                )
            )

        scored.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        recommendations = []

        for score, item in scored[:top_k]:

            recommendations.append(
                {
                    "name": item.get(
                        "name",
                        ""
                    ),

                    "url": item.get(
                        "link",
                        ""
                    ),

                    "description": item.get(
                        "description",
                        ""
                    ),

                    "duration": item.get(
                        "duration",
                        ""
                    ),

                    "job_levels": item.get(
                        "job_levels",
                        []
                    ),

                    "remote": item.get(
                        "remote",
                        "unknown"
                    ),

                    "adaptive": item.get(
                        "adaptive",
                        "unknown"
                    ),

                    "keys": item.get(
                        "keys",
                        []
                    ),

                    "score": score
                }
            )

        return recommendations