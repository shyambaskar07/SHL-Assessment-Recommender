from app.services.recommender import (
    Recommender
)

from app.models.conversation_state import (
    ConversationState
)

state = ConversationState(
    role="Java Developer",
    seniority="Mid-Level",
    technical_required=True,
    communication_required=True,
    personality_required=False,
    leadership_required=False
)

recommender = Recommender()

results = recommender.recommend(
    state
)

print()

for idx, item in enumerate(
    results,
    start=1
):
    print(
        f"{idx}. {item['name']}"
    )