from app.services.clarification import (
    ClarificationService
)

from app.models.conversation_state import (
    ConversationState
)


state = ConversationState(
    role="Java Developer"
)

clarifier = ClarificationService()

question = clarifier.generate_question(
    state
)

print(question)