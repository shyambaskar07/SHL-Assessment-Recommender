class Ranker:

    def score(
        self,
        assessment,
        state
    ):

        score = 0

        name = assessment.get(
            "name",
            ""
        ).lower()

        description = assessment.get(
            "description",
            ""
        ).lower()

        text = (
            name
            + " "
            + description
        )

        job_levels = [
            level.lower()
            for level in assessment.get(
                "job_levels",
                []
            )
        ]

        categories = [
            key.lower()
            for key in assessment.get(
                "keys",
                []
            )
        ]

        # ----------------------------
        # Exact role matching
        # ----------------------------

        if state.role:

            role = state.role.lower()

            if "java" in role:

                if (
                    "java" in name
                    or "java " in description
                ):
                    score += 20

                if "javascript" in text:
                    score -= 25

            if "python" in role:

                if "python" in text:
                    score += 20

            if "developer" in role:

                if (
                    "technical" in text
                    or "programming" in text
                    or "coding" in text
                ):
                    score += 10

            for word in role.split():

                if (
                    len(word) > 3
                    and word in text
                ):
                    score += 3

        # ----------------------------
        # Technical requirements
        # ----------------------------

        if state.technical_required:

            technical_words = [
                "technical",
                "programming",
                "coding",
                "developer",
                "software",
                "knowledge & skills"
            ]

            for word in technical_words:

                if (
                    word in text
                    or word in categories
                ):
                    score += 3

        # ----------------------------
        # Communication requirements
        # ----------------------------

        if state.communication_required:

            communication_words = [
                "communication",
                "stakeholder",
                "interaction",
                "collaboration",
                "client",
                "presentation"
            ]

            for word in communication_words:

                if word in text:
                    score += 4

            if (
                "competencies"
                in categories
            ):
                score += 5

        # ----------------------------
        # Personality requirements
        # ----------------------------

        if state.personality_required:

            personality_words = [
                "personality",
                "behavior",
                "opq",
                "motivation"
            ]

            for word in personality_words:

                if word in text:
                    score += 5

            if (
                "personality & behavior"
                in categories
            ):
                score += 10

        # ----------------------------
        # Leadership requirements
        # ----------------------------

        if state.leadership_required:

            leadership_words = [
                "leadership",
                "manager",
                "management",
                "supervisor"
            ]

            for word in leadership_words:

                if word in text:
                    score += 5

        # ----------------------------
        # Seniority matching
        # ----------------------------

        if state.seniority:

            seniority = (
                state.seniority.lower()
            )

            if (
                "mid" in seniority
                and any(
                    "mid"
                    in level
                    for level in job_levels
                )
            ):
                score += 8

            elif (
                "entry" in seniority
                and any(
                    "entry"
                    in level
                    for level in job_levels
                )
            ):
                score += 8

            elif (
                "manager" in seniority
                and any(
                    "manager"
                    in level
                    for level in job_levels
                )
            ):
                score += 8

        # ----------------------------
        # Small boost for remote
        # ----------------------------

        if (
            assessment.get(
                "remote",
                "no"
            ) == "yes"
        ):
            score += 1

        return score