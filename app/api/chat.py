from fastapi import APIRouter

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse

from app.services.state_builder import StateBuilder
from app.services.intent_router import IntentRouter
from app.services.clarification import ClarificationService
from app.services.recommender import Recommender

router = APIRouter()

state_builder = StateBuilder()
intent_router = IntentRouter()
clarifier = ClarificationService()
recommender = Recommender()


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

        state = state_builder.build(
            request.messages
        )

        intent = intent_router.route(
            state,
            request.messages
        )

        print("\n===== STATE =====")
        print(state)

        print("\n===== INTENT =====")
        print(intent)

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

        elif intent == "compare":

            return ChatResponse(
                reply=(
                    "Comparison between "
                    "assessments will be "
                    "supported in a future "
                    "update."
                ),
                recommendations=[],
                end_of_conversation=False
            )

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

    except Exception:

        user_message = ""

        if messages:
            user_message = messages[-1].content.lower()

        # vague hiring request
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

            reply = {
                "reply":
                    (
                        "I can help recommend SHL assessments. "
                        "Please provide the target role, seniority level, "
                        "required technical skills, and whether leadership "
                        "or stakeholder interaction is important."
                    ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # comparison request
        elif any(
            word in user_message
            for word in [
                "compare",
                "difference",
                "vs",
                "versus"
            ]
        ):

            reply = {
                "reply":
                    (
                        "I can compare SHL assessments if you provide "
                        "two SHL assessment names."
                    ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # prompt injection or off-topic
        elif any(
            word in user_message
            for word in [
                "aws",
                "azure",
                "certification",
                "ignore previous instructions"
            ]
        ):

            reply = {
                "reply":
                    (
                        "I can only recommend and compare SHL assessments "
                        "available in the SHL catalog."
                    ),
                "recommendations": [],
                "end_of_conversation": True
            }

        # empty message
        elif user_message.strip() == "":

            reply = {
                "reply":
                    (
                        "Please describe the role or hiring requirement "
                        "for which you need SHL assessments."
                    ),
                "recommendations": [],
                "end_of_conversation": False
            }

        # generic fallback
        else:

            reply = {
                "reply":
                    (
                        "I need more information before recommending "
                        "assessments. Please provide details such as "
                        "role, seniority, technical skills, leadership "
                        "requirements, and stakeholder interaction."
                    ),
                "recommendations": [],
                "end_of_conversation": False
            }