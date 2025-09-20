from pydantic import BaseModel
from typing import Dict, Any


class ExtractEntitiesRequest(BaseModel):
    text: str

class ExtractEntitiesResponse(BaseModel):
    entities: Dict[str, Any]