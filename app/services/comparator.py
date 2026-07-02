class Comparator:

    def compare(
        self,
        assessment1,
        assessment2
    ):

        if (
            assessment1 is None
            or assessment2 is None
        ):
            return {
                "error":
                    "Two valid "
                    "assessments "
                    "are required "
                    "for comparison."
            }

        result = {

            "assessment_1": {

                "name":
                    assessment1.get(
                        "name",
                        ""
                    ),

                "duration":
                    assessment1.get(
                        "duration",
                        ""
                    ),

                "job_levels":
                    assessment1.get(
                        "job_levels",
                        []
                    ),

                "remote":
                    assessment1.get(
                        "remote",
                        "unknown"
                    ),

                "adaptive":
                    assessment1.get(
                        "adaptive",
                        "unknown"
                    ),

                "categories":
                    assessment1.get(
                        "keys",
                        []
                    )
            },

            "assessment_2": {

                "name":
                    assessment2.get(
                        "name",
                        ""
                    ),

                "duration":
                    assessment2.get(
                        "duration",
                        ""
                    ),

                "job_levels":
                    assessment2.get(
                        "job_levels",
                        []
                    ),

                "remote":
                    assessment2.get(
                        "remote",
                        "unknown"
                    ),

                "adaptive":
                    assessment2.get(
                        "adaptive",
                        "unknown"
                    ),

                "categories":
                    assessment2.get(
                        "keys",
                        []
                    )
            }
        }

        return result