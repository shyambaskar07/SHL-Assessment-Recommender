import json
import re

from app.services.llm_service import LLMService
from app.models.conversation_state import ConversationState


class StateBuilder:

    def __init__(self):
        self.llm = LLMService()

    def build(self, messages):

        conversation = "\n".join(
            [
                f"{m.role}: {m.content}"
                for m in messages
            ]
        )

        prompt = f"""
Extract hiring requirements from the conversation.

Return ONLY valid JSON.

If there are multiple roles, return a JSON array.

Do NOT include:
- markdown
- code fences
- explanations
- comments
- extra text

Rules:
- role should be the job role.
- seniority should be one of:
  Entry-Level, Graduate, Mid-Level, Senior, Manager, Director, Executive
- experience_years should be an integer or null.
- technical_required should be true or false.
- communication_required should be true or false.
- personality_required should be true or false.
- leadership_required should be true or false.

Example output:

{{
    "role": "Java Developer",
    "seniority": "Mid-Level",
    "experience_years": 4,
    "technical_required": true,
    "communication_required": true,
    "personality_required": false,
    "leadership_required": false
}}

Conversation:

{conversation}
"""

        response = self.llm.generate(prompt)

        print("\n===== GEMINI RESPONSE =====")
        print(response)
        print("===========================\n")

        json_match = re.search(
            r'(\[.*\]|\{.*\})',
            response,
            re.DOTALL
        )

        if not json_match:
            raise ValueError(
                f"No JSON found in Gemini response:\n{response}"
            )

        data = json.loads(
            json_match.group()
        )

        # Handle multiple extracted roles
        if isinstance(
            data,
            list
        ):
            data = data[0]

        technical_required = data.get(
            "technical_required"
        )

        communication_required = data.get(
            "communication_required"
        )

        personality_required = data.get(
            "personality_required"
        )

        leadership_required = data.get(
            "leadership_required"
        )

        if isinstance(
            technical_required,
            str
        ):
            technical_required = True

        if isinstance(
            communication_required,
            str
        ):
            communication_required = True

        if technical_required is None:
            technical_required = False

        if communication_required is None:
            communication_required = False

        if personality_required is None:
            personality_required = False

        if leadership_required is None:
            leadership_required = False

        return ConversationState(
        role=data.get("role") or "General Hiring",
        seniority=data.get("seniority") or "Graduate",
        experience_years=data.get("experience_years"),
        technical_required=technical_required,
        communication_required=communication_required,
        personality_required=personality_required,
        leadership_required=leadership_required
        )