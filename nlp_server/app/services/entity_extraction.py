import re
import spacy
from nlp_server.app.models.entity_model import ExtractEntitiesRequest, ExtractEntitiesResponse
from typing import Dict, Any


nlp = spacy.load("ru_core_news_sm")


def extract_entities_spacy(text: str) -> Dict[str, Any]:
    """Извлечение сущностей с помощью spaCy"""
    if not nlp:
        return {}

    doc = nlp(text)
    entities = {}

    for ent in doc.ents:
        if ent.label_ == "MONEY":
            entities["sum"] = ent.text
        elif ent.label_ == "PRODUCT":
            entities["product"] = ent.text
        elif ent.label_ == "ORG":
            entities["company"] = ent.text

    return entities


def extract_entities_regex(text: str) -> Dict[str, Any]:
    """Извлечение сущностей с помощью регулярных выражений"""
    entities = {}

    # Поиск сумм
    money_patterns = [
        r'(\d+)\s*тыс',
        r'(\d+)\s*т\.р',
        r'на\s+(\d+)\s+руб',
        r'сумм[аой]\s+(\d+)'
    ]

    for pattern in money_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = int(match.group(1))
            if 'тыс' in pattern or 'т.р' in pattern:
                amount *= 1000
            entities["sum"] = amount
            break

    # Поиск продуктов
    product_keywords = ['на поставку', 'на закупку', 'товар', 'продукт']
    for keyword in product_keywords:
        if keyword in text.lower():
            # Берем текст после ключевого слова
            start_idx = text.lower().find(keyword) + len(keyword)
            product_text = text[start_idx:].split('.')[0].split(' на ')[0].strip()
            if product_text and len(product_text) > 2:
                entities["product"] = product_text
                break

    return entities


def extract_entities(text: str) -> ExtractEntitiesResponse:
    """Основная функция извлечения сущностей"""
    entities = {}

    # Пробуем разные методы
    if nlp:
        entities.update(extract_entities_spacy(text))

    entities.update(extract_entities_regex(text))

    return ExtractEntitiesResponse(entities=entities)