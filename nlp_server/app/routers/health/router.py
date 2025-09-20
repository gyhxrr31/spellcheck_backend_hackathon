from nlp_server.app.models.process_text_model import HealthResponse
from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["List of available models and server status"]
)

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Проверка статуса сервера и версий моделей"""
    return {
        "status": "healthy",
        "model_versions": {
            "intent_classifier": "1.0",
            "entity_extractor": "1.0",
            "spell_checker": "1.0"
        }
    }