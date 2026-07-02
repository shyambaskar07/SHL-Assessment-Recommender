from pydantic import BaseModel
from typing import List, Optional


class Recommendation(BaseModel):
    name: str
    url: str
    description: Optional[str] = ""
    duration: Optional[str] = ""
    job_levels: List[str] = []
    remote: Optional[str] = ""
    adaptive: Optional[str] = ""
    keys: List[str] = []
    score: Optional[int] = 0


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool


class HealthResponse(BaseModel):
    status: str