from fastapi import APIRouter, HTTPException
from nlp_server.app.models.process_text_model import ProcessTextRequest, ProcessTextResponse
from nlp_server.app.services.spell_checker import correct_spelling
from nlp_server.app.services.intent_classifier import classify_intent
from nlp_server.app.services.entity_extraction import extract_entities
from loguru import logger


router = APIRouter(
    prefix="/process",
    tags=["Processing native language route"]
)


@router.post("/", response_model=ProcessTextResponse)
async def process_text(request: ProcessTextRequest):
    """
    Основной эндпоинт для обработки текста
    """
    try:
        result = {
            "original_text": request.text,
            "processed_text": request.text,
            "intent": "unknown",
            "confidence": 0.0,
            "entities": {},
            "spellcheck_corrections": {}
        }

        # Исправление опечаток
        if "spellcheck" in request.tasks:
            spell_result = correct_spelling(request.text)
            result["processed_text"] = spell_result.corrected_text
            result["spellcheck_corrections"] = spell_result.corrections

        # Классификация намерения
        if "intent" in request.tasks:
            intent_result = classify_intent(result["processed_text"])
            result["intent"] = intent_result.intent
            result["confidence"] = intent_result.confidence

        # Извлечение сущностей
        if "entities" in request.tasks:
            entity_result = extract_entities(result["processed_text"])
            result["entities"] = entity_result.entities

        logger.info(f"Processed text: {request.text} -> Intent: {result['intent']}")
        return result

    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))