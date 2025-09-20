from nlp_server.app.services.spell_checker import correct_spelling
from nlp_server.app.models.spell_checker_model import BulkSpellCheckRequest, BulkSpellCheckResponse, SpellCheckResult
from fastapi import APIRouter, HTTPException
from loguru import logger



router = APIRouter(
    prefix="/spellcheck",
    tags=["Check spelling route"]
)


@router.post("/")
async def spellcheck(text: str):
    """Исправление опечаток в одном тексте"""
    try:
        result = correct_spelling(text)
        return result.dict()
    except Exception as e:
        logger.error(f"Error in spellcheck: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk", response_model=BulkSpellCheckResponse)
async def bulk_spellcheck(request: BulkSpellCheckRequest):
    """Массовое исправление опечаток"""
    try:
        results = []
        successful = 0
        failed = 0

        for text in request.texts:
            try:
                result = correct_spelling(text)
                results.append(SpellCheckResult(
                    original_text=result.original_text,
                    corrected_text=result.corrected_text,
                    corrections=result.corrections,
                    confidence=result.confidence
                ))
                successful += 1
            except Exception as e:
                results.append(SpellCheckResult(
                    original_text=text,
                    corrected_text=text,
                    corrections={},
                    confidence=0.0,
                    error=str(e)
                ))
                failed += 1

        return BulkSpellCheckResponse(
            results=results,
            total_processed=len(request.texts),
            successful=successful,
            failed=failed
        )
    except Exception as e:
        logger.error(f"Error in bulk spellcheck: {e}")
        raise HTTPException(status_code=500, detail=str(e))