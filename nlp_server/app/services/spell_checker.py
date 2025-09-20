from spellchecker import SpellChecker
from nlp_server.app.models.spell_checker_model import CorrectSpellingRequest, CorrectSpellingResponse
from typing import List
import re


spell = SpellChecker(language="ru")

domain_words = [
    'кс', 'котировочная', 'сессия', 'эцп', 'электронная', 'цифровая', 'подпись',
    'закупка', 'тендер', 'поставщик', 'заказчик', 'канцелярия', 'канцелярские',
    'оргтехника', 'ремонт', 'профиль', 'компания', 'создай', 'создать', 'найди',
    'найти', 'покажи', 'показать', 'добавь', 'добавить', 'измени', 'изменить',
    'товары', 'услуги', 'работы', 'поставка', 'проект', 'договор', 'контракт',
    'цена', 'стоимость', 'бюджет', 'сумма', 'рублей', 'тысяч', 'миллион',
    'аукцион', 'конкурс', 'заявка', 'предложение', 'результат', 'победитель'
]


for word in domain_words:
    spell.word_frequency.add(word)


def correct_spelling(text: str) -> CorrectSpellingResponse:
    """
    Исправление опечаток в тексте с использованием pyspellchecker
    """
    # Разбиваем текст на слова с сохранением разделителей
    words = re.findall(r'\b\w+\b|[^\w\s]', text)
    corrections = {}
    total_words = 0
    corrected_words = 0

    corrected_parts = []

    for word in words:
        # Пропускаем не-слова (знаки препинания и т.д.)
        if not re.match(r'\w+', word):
            corrected_parts.append(word)
            continue

        total_words += 1

        # Пропускаем числа и короткие слова
        if word.isdigit() or len(word) < 2:
            corrected_parts.append(word)
            continue

        # Проверяем, известно ли слово (учитывая доменный словарь)
        known = spell.known([word.lower()])

        if not known:
            # Ищем кандидатов на исправление
            candidates = spell.candidates(word.lower())
            if candidates:
                # Берем самый вероятный вариант
                best_candidate = spell.correction(word.lower())
                if best_candidate and best_candidate != word.lower():
                    # Сохраняем оригинальное написание (с заглавными буквами)
                    if word[0].isupper():
                        best_candidate = best_candidate.capitalize()

                    corrections[word] = best_candidate
                    corrected_parts.append(best_candidate)
                    corrected_words += 1
                else:
                    corrected_parts.append(word)
            else:
                corrected_parts.append(word)
        else:
            corrected_parts.append(word)

    # Собираем исправленный текст
    corrected_text = ''.join(corrected_parts)

    # Вычисляем уверенность (доля исправленных слов от общего числа слов)
    confidence = 1.0 - (corrected_words / total_words) if total_words > 0 else 1.0

    return CorrectSpellingResponse(
        original_text=text,
        corrected_text=corrected_text,
        corrections=corrections,
        confidence=confidence
    )


def bulk_correct_spelling(texts: List[str]) -> List[CorrectSpellingResponse]:
    """
    Массовое исправление опечаток для нескольких текстов
    """
    return [correct_spelling(text) for text in texts]


# Пример использования
if __name__ == "__main__":
    # Тестовые примеры с опечатками
    test_cases = [
        "Создай КС на 300 тыщ на канцелярские товара",
        "Найди котировочную сесию по оргтехнике",
        "Добавь ЭЦП для новой компании",
        "Создай закупку на ремонт офиса на 500 тыс руб",
        "Покажи историю закупук за последний месяц"
    ]

    for test in test_cases:
        result = correct_spelling(test)
        print(f"Оригинал: {test}")
        print(f"Исправлено: {result.corrected_text}")
        print(f"Исправления: {result.corrections}")
        print(f"Уверенность: {result.confidence:.2f}")
        print("-" * 50)