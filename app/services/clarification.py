from app.models.conversation_state import ConversationState


class ClarificationService:

    def generate_question(
        self,
        state: ConversationState
    ):

        missing = []

        if not state.role:
            missing.append(
                "the role you are hiring for"
            )

        if not state.seniority:
            missing.append(
                "the seniority level"
            )

        if not state.technical_required:
            missing.append(
                "whether technical skills should be assessed"
            )

        if not state.communication_required:
            missing.append(
                "whether communication or stakeholder interaction skills are important"
            )

        if not state.personality_required:
            missing.append(
                "whether personality or behavioral assessments are needed"
            )

        if len(missing) == 0:
            return None

        question = (
            "To recommend the most suitable SHL assessments, "
            "could you provide information about:\n\n"
        )

        for idx, item in enumerate(
            missing,
            start=1
        ):
            question += (
                f"{idx}. {item}\n"
            )

        return question