from app.services.guardrails import Guardrails


class IntentRouter:

    def __init__(self):
        self.guardrails = Guardrails()

    def route(
        self,
        state,
        messages
    ):

        latest_message = (
            messages[-1].content.lower()
        )

        # --------------------
        # Guardrails
        # --------------------

        if self.guardrails.is_blocked(
            latest_message
        ):
            return "refuse"

        # --------------------
        # Comparison requests
        # --------------------

        comparison_words = [
            "compare",
            "difference",
            "vs",
            "versus"
        ]

        for word in comparison_words:
            if word in latest_message:
                return "compare"

        # --------------------
        # Refinement requests
        # --------------------

        refinement_words = [
            "also",
            "add",
            "include",
            "along with"
        ]

        for word in refinement_words:
            if word in latest_message:
                return "refine"

        # --------------------
        # Clarification rules
        # --------------------

        seniority_words = [
            "entry",
            "entry-level",
            "graduate",
            "junior",
            "mid",
            "mid-level",
            "senior",
            "manager",
            "director",
            "executive"
        ]

        has_seniority = False

        for word in seniority_words:
            if word in latest_message:
                has_seniority = True
                break

        communication_words = [
            "stakeholder",
            "communication",
            "client",
            "collaboration",
            "presentation"
        ]

        has_communication = False

        for word in communication_words:
            if word in latest_message:
                has_communication = True
                break

        technical_words = [
            "developer",
            "engineer",
            "programmer",
            "technical",
            "coding",
            "java",
            "python",
            "c++",
            "javascript"
        ]

        has_technical = False

        for word in technical_words:
            if word in latest_message:
                has_technical = True
                break

        personality_words = [
            "personality",
            "behavior",
            "leadership",
            "managerial"
        ]

        has_personality = False

        for word in personality_words:
            if word in latest_message:
                has_personality = True
                break

        # If only a generic role is mentioned,
        # ask for more information.

        if not has_seniority:
            return "clarify"

        if not (
            has_technical or
            has_communication or
            has_personality
        ):
            return "clarify"

        return "recommend"