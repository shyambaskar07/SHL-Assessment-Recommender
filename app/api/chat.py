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

        question = clarifier.generate_question(
            state
        )

        return ChatResponse(
            reply=question,
            recommendations=[],
            end_of_conversation=False
        )

    elif intent == "recommend":

        recommendations = recommender.recommend(
            state
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
                "Comparison feature "
                "implemented in Batch 10. "
                "Entity extraction for "
                "assessment names will be "
                "added next."
            ),
            recommendations=[],
            end_of_conversation=False
        )

    elif intent == "refine":

        recommendations = recommender.recommend(
            state
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