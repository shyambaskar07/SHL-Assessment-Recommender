from app.services.state_builder import (
    StateBuilder
)

messages = [
    type(
        "Message",
        (),
        {
            "role": "user",
            "content":
            "Hiring a Java developer "
            "who works with stakeholders"
        }
    ),
    type(
        "Message",
        (),
        {
            "role": "assistant",
            "content":
            "What seniority level?"
        }
    ),
    type(
        "Message",
        (),
        {
            "role": "user",
            "content":
            "Mid-level with 4 years "
            "experience"
        }
    )
]

state = StateBuilder().build(
    messages
)

print(state)