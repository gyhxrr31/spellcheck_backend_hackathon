from pydantic import BaseModel
from typing import Dict, List, Optional


class ClassifyIntentRequest(BaseModel):
    text: str

class ClassifyIntentResponse(BaseModel):
    intent: str
    confidence: float
    possible_intents: Dict[str, float]
    keywords: List[str]
