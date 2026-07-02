from app.services.intent_router import (
    IntentRouter
)

from app.models.conversation_state import (
    ConversationState
)

messages = [
    type(
        "Message",
        (),
        {
            "role": "user",
            "content":
            "Need tests for a Java developer"
        }
    )
]

state = ConversationState(
    role="Java Developer",
    seniority="Mid-Level"
)

router = IntentRouter()

intent = router.route(
    state,
    messages
)

print(
    "Intent:",
    intent
)