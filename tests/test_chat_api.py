from app.models.request_models import (
    Message
)

from app.services.state_builder import (
    StateBuilder
)

messages = [
    Message(
        role="user",
        content=(
            "Need assessments for "
            "a mid-level Java developer "
            "working with stakeholders"
        )
    )
]

state = (
    StateBuilder()
    .build(messages)
)

print(state)