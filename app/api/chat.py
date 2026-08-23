from fastapi import APIRouter

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse

from app.services.state_builder import StateBuilder
from app.services.intent_router import IntentRouter
from app.services.clarification import ClarificationService
from app.services.recommender import Recommender
from app.services.comparator import Comparator
from app.services.retriever import Retriever


router = APIRouter()

state_builder = StateBuilder()
intent_router = IntentRouter()
clarifier = ClarificationService()
recommender = Recommender()
comparator = Comparator()
retriever = Retriever()


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:

        if (
            not request.messages
            or len(request.messages) == 0
        ):
            return ChatResponse(
                reply=(
                    "Please provide hiring "
                    "requirements."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        if (
            request.messages[-1].content
            is None
        ):
            return ChatResponse(
                reply=(
                    "Please provide hiring "
                    "requirements."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        if (
            request.messages[-1]
            .content.strip()
            == ""
        ):
            return ChatResponse(
                reply=(
                    "Please provide hiring "
                    "requirements."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        # Detect intent first
        intent = intent_router.route(
            None,
            request.messages
        )

        print("\n===== INTENT =====")
        print(intent)

        # --------------------
        # Comparison
        # --------------------

        if intent == "compare":

            user_message = (
                request.messages[-1]
                .content
            )

            assessments = (
                retriever.find_in_query(
                    user_message
                )
            )

            print(
                "\n===== COMPARISON ASSESSMENTS ====="
            )

            for assessment in assessments:
                print(
                    assessment.get(
                        "name",
                        ""
                    )
                )

            if len(assessments) < 2:

                return ChatResponse(
                    reply=(
                        "I could not find two "
                        "valid SHL assessments "
                        "in the catalogue. "
                        "Please provide the exact "
                        "assessment names."
                    ),
                    recommendations=[],
                    end_of_conversation=False
                )

            assessment1 = assessments[0]
            assessment2 = assessments[1]

            comparison = comparator.compare(
                assessment1,
                assessment2
            )

            a1 = comparison[
                "assessment_1"
            ]

            a2 = comparison[
                "assessment_2"
            ]

            reply = (
                f"Comparison between "
                f"{a1['name']} and "
                f"{a2['name']}:\n\n"

                f"1. Duration:\n"
                f"- {a1['name']}: "
                f"{a1['duration']}\n"
                f"- {a2['name']}: "
                f"{a2['duration']}\n\n"

                f"2. Job Levels:\n"
                f"- {a1['name']}: "
                f"{', '.join(a1['job_levels'])}\n"
                f"- {a2['name']}: "
                f"{', '.join(a2['job_levels'])}\n\n"

                f"3. Remote:\n"
                f"- {a1['name']}: "
                f"{a1['remote']}\n"
                f"- {a2['name']}: "
                f"{a2['remote']}\n\n"

                f"4. Adaptive:\n"
                f"- {a1['name']}: "
                f"{a1['adaptive']}\n"
                f"- {a2['name']}: "
                f"{a2['adaptive']}\n\n"

                f"5. Categories:\n"
                f"- {a1['name']}: "
                f"{', '.join(a1['categories'])}\n"
                f"- {a2['name']}: "
                f"{', '.join(a2['categories'])}\n\n"

                f"6. Description:\n"
                f"- {a1['name']}: "
                f"{a1['description']}\n"
                f"- {a2['name']}: "
                f"{a2['description']}"
            )

            return ChatResponse(
                reply=reply,
                recommendations=[],
                end_of_conversation=True
            )

        # --------------------
        # Build state
        # --------------------

        state = state_builder.build(
            request.messages
        )

        print("\n===== STATE =====")
        print(state)

        # --------------------
        # Clarify
        # --------------------

        if intent == "clarify":

            question = (
                clarifier
                .generate_question(
                    state
                )
            )

            return ChatResponse(
                reply=question,
                recommendations=[],
                end_of_conversation=False
            )

        # --------------------
        # Recommend
        # --------------------

        elif intent == "recommend":

            recommendations = (
                recommender
                .recommend(
                    state
                )
            )

            reply = (
                f"Based on your requirements, "
                f"I recommend the following "
                f"SHL assessments for "
                f"{state.role or 'the role'}."
            )

            return ChatResponse(
                reply=reply,
                recommendations=recommendations,
                end_of_conversation=True
            )

        # --------------------
        # Refine
        # --------------------

        elif intent == "refine":

            recommendations = (
                recommender
                .recommend(
                    state
                )
            )

            return ChatResponse(
                reply=(
                    "Updated recommendations "
                    "based on your additional "
                    "requirements."
                ),
                recommendations=recommendations,
                end_of_conversation=False
            )

        # --------------------
        # Refuse
        # --------------------

        elif intent == "refuse":

            return ChatResponse(
                reply=(
                    "I can only recommend and "
                    "compare SHL assessments "
                    "available in the SHL catalogue."
                ),
                recommendations=[],
                end_of_conversation=True
            )

        else:

            return ChatResponse(
                reply=(
                    "I can only recommend "
                    "assessments available "
                    "in the SHL catalog."
                ),
                recommendations=[],
                end_of_conversation=False
            )

    except Exception as e:

        print(
            "\n===== CHAT ERROR ====="
        )

        print(e)

        user_message = ""

        if request.messages:

            user_message = (
                request.messages[-1]
                .content
                .lower()
            )

        if any(
            word in user_message
            for word in [
                "hire",
                "hiring",
                "recruit",
                "candidate",
                "assessment"
            ]
        ):

            return ChatResponse(
                reply=(
                    "I can help recommend SHL "
                    "assessments. Please provide "
                    "the target role, seniority level, "
                    "required technical skills, and "
                    "whether leadership or stakeholder "
                    "interaction is important."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        elif any(
            word in user_message
            for word in [
                "compare",
                "difference",
                "vs",
                "versus"
            ]
        ):

            return ChatResponse(
                reply=(
                    "I can compare SHL assessments "
                    "if you provide two SHL "
                    "assessment names."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        elif any(
            word in user_message
            for word in [
                "aws",
                "azure",
                "certification",
                "ignore previous instructions"
            ]
        ):

            return ChatResponse(
                reply=(
                    "I can only recommend and "
                    "compare SHL assessments "
                    "available in the SHL catalog."
                ),
                recommendations=[],
                end_of_conversation=True
            )

        elif user_message.strip() == "":

            return ChatResponse(
                reply=(
                    "Please describe the role or "
                    "hiring requirement for which "
                    "you need SHL assessments."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        else:

            return ChatResponse(
                reply=(
                    "I need more information before "
                    "recommending assessments. Please "
                    "provide details such as role, "
                    "seniority, technical skills, "
                    "leadership requirements, and "
                    "stakeholder interaction."
                ),
                recommendations=[],
                end_of_conversation=False
            )
