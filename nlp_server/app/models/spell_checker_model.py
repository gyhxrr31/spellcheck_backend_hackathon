from pydantic import BaseModel
from typing import Dict, List, Optional

class CorrectSpellingRequest(BaseModel):
    text: str


class SpellCheckResult(BaseModel):
    original_text: str
    corrected_text: str
    corrections: Dict[str, str]
    confidence: float
    error: Optional[str] = None


class CorrectSpellingResponse(BaseModel):
    original_text: str
    corrected_text: str
    corrections: Dict[str, str]


class BulkSpellCheckRequest(BaseModel):
    texts: List[str]


class BulkSpellCheckResponse(BaseModel):
    results: List[SpellCheckResult]
    total_processed: int
    successful: int
    failed: int