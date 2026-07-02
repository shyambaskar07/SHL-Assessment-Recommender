import os

from app.models.request_models import Message
from app.services.state_builder import StateBuilder
from app.services.intent_router import IntentRouter
from app.services.recommender import Recommender
from app.services.clarification import ClarificationService


state_builder = StateBuilder()
intent_router = IntentRouter()
recommender = Recommender()
clarifier = ClarificationService()


conversation_folder = "GenAI_SampleConversations"


for filename in sorted(
    os.listdir(conversation_folder)
):

    if not filename.endswith(".md"):
        continue

    print("\n" + "=" * 80)
    print("Conversation:", filename)
    print("=" * 80)

    with open(
        os.path.join(
            conversation_folder,
            filename
        ),
        "r",
        encoding="utf-8"
    ) as f:
        text = f.read()

    messages = [
        Message(
            role="user",
            content=text
        )
    ]

    state = state_builder.build(
        messages
    )

    intent = intent_router.route(
        state,
        messages
    )

    print("\nIntent:", intent)

    if intent == "clarify":

        question = (
            clarifier.generate_question(
                state
            )
        )

        print("\nClarification:")
        print(question)

    elif intent == "recommend":

        recommendations = (
            recommender.recommend(
                state
            )
        )

        print("\nTop Recommendations:\n")

        for idx, rec in enumerate(
            recommendations[:5],
            1
        ):
            print(
                f"{idx}. "
                f"{rec['name']}"
            )

    elif intent == "compare":

        print(
            "\nComparison conversation "
            "detected."
        )

    elif intent == "refuse":

        print(
            "\nRequest rejected by "
            "guardrails."
        )