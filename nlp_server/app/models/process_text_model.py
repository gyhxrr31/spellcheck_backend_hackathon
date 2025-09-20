from pydantic import BaseModel
from typing import List, Dict, Any


class ProcessTextRequest(BaseModel):
    text: str
    tasks: List[str] = ["spellcheck", "intent", "entities"]



class ProcessTextResponse(BaseModel):
    original_text: str
    processed_text: str
    intent: str
    confidence: float
    entities: Dict[str, Any]
    spellcheck_corrections: Dict[str, str]


class HealthResponse(BaseModel):
    status: str
    model_versions: Dict[str, str]