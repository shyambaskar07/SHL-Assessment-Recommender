from pydantic import BaseModel
from typing import Optional


class ConversationState(BaseModel):

    role: Optional[str] = None

    seniority: Optional[str] = None

    experience_years: Optional[int] = None

    technical_required: bool = False

    communication_required: bool = False

    personality_required: bool = False

    leadership_required: bool = False