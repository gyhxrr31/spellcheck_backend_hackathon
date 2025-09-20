from nlp_server.app.models.classfier_model import ClassifyIntentRequest, ClassifyIntentResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from typing import List
import joblib
import os

# Правила для fallback классификации
ACTION_KEYWORDS = [
    'создай', 'создать', 'добавь', 'добавить', 'измени', 'изменить',
    'удали', 'удалить', 'обнови', 'обновить', 'зарегистрируй', 'зарегистрировать'
]

SEARCH_KEYWORDS = [
    'найди', 'найти', 'покажи', 'показать', 'ищи', 'искать', 'выведи',
    'вывести', 'открой', 'открыть', 'посмотри', 'посмотреть', 'что такое',
    'где', 'как', 'поиск', 'найти'
]


# Обучение простой модели
def train_intent_model():
    """Обучение модели классификации намерений"""
    train_texts = [
        # Action intent examples (15 примеров)
        "создай котировочную сессию", "создай кс на канцелярию", "добавь новую компанию",
        "хочу создать закупку на мебель", "измени профиль компании", "надо создать кс",
        "создать закупку", "добавить эцп", "создай кс на 100000", "создай заявку на ремонт",
        "добавь электронную подпись", "создай новый профиль", "измени данные компании",
        "зарегистрируй новую организацию", "обнови информацию о закупке",

        # Search intent examples (15 примеров)
        "покажи мои закупки", "найди котировочные сессии", "ищу поставщиков мебели",
        "что такое кс", "история закупок", "найди кс по канцелярии", "покажи компании",
        "выведи все закупки", "информация о кс", "поиск товаров", "найти поставщика",
        "покажи историю запросов", "что значит эцп", "как создать закупку",
        "где посмотреть результаты тендера"
    ]

    # 1 - action, 0 - search (ровно 30 меток для 30 текстов)
    train_labels = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  # 15 action
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 15 search
    ]

    # Проверка соответствия размеров
    if len(train_texts) != len(train_labels):
        raise ValueError(f"Несоответствие размеров: texts={len(train_texts)}, labels={len(train_labels)}")

    print(f"Обучение модели на {len(train_texts)} примерах...")

    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=500,
            stop_words=None,
            min_df=1,
            max_df=0.8
        )),
        ('clf', LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'
        ))
    ])

    model.fit(train_texts, train_labels)
    print("Модель успешно обучена!")
    return model


def rule_based_intent_classification(text: str) -> ClassifyIntentResponse:
    """Классификация намерения на основе правил (fallback)"""
    text_lower = text.lower()

    action_count = sum(1 for keyword in ACTION_KEYWORDS if keyword in text_lower)
    search_count = sum(1 for keyword in SEARCH_KEYWORDS if keyword in text_lower)

    if action_count > search_count:
        confidence = min(0.9, 0.5 + (action_count / len(ACTION_KEYWORDS)))
        return ClassifyIntentResponse(
            intent="action",
            confidence=round(confidence, 2),
            possible_intents={"action": confidence, "search": 1 - confidence},
            keywords=[kw for kw in ACTION_KEYWORDS if kw in text_lower]
        )
    elif search_count > action_count:
        confidence = min(0.9, 0.5 + (search_count / len(SEARCH_KEYWORDS)))
        return ClassifyIntentResponse(
            intent="search",
            confidence=round(confidence, 2),
            possible_intents={"action": 1 - confidence, "search": confidence},
            keywords=[kw for kw in SEARCH_KEYWORDS if kw in text_lower]
        )
    else:
        # Если количество ключевых слов одинаковое или их нет
        return ClassifyIntentResponse(
            intent="unknown",
            confidence=0.5,
            possible_intents={"action": 0.5, "search": 0.5},
            keywords=[]
        )


# Загрузка или обучение модели
model = None
model_path = "intent_model.joblib"


def initialize_model():
    """Инициализация модели с обработкой ошибок"""
    global model
    try:
        if os.path.exists(model_path):
            print("Загрузка существующей модели...")
            model = joblib.load(model_path)
            print("Модель успешно загружена!")
        else:
            print("Обучение новой модели...")
            model = train_intent_model()
            joblib.dump(model, model_path)
            print("Модель обучена и сохранена!")
    except Exception as e:
        print(f"Ошибка инициализации ML модели: {e}")
        print("Используется rule-based классификация")
        model = None


# Инициализируем модель при импорте
initialize_model()


def classify_intent(text: str) -> ClassifyIntentResponse:
    """Классификация намерения пользователя"""

    # Если модель доступна, используем ML
    if model is not None:
        try:
            prediction = model.predict_proba([text])[0]
            intent_label = model.predict([text])[0]

            intent = "action" if intent_label == 1 else "search"
            confidence = float(prediction[intent_label])

            # Извлекаем ключевые слова
            text_lower = text.lower()
            all_keywords = ACTION_KEYWORDS + SEARCH_KEYWORDS
            keywords = [kw for kw in all_keywords if kw in text_lower]

            return ClassifyIntentResponse(
                intent=intent,
                confidence=round(confidence, 2),
                possible_intents={
                    "action": float(prediction[1]),
                    "search": float(prediction[0])
                },
                keywords=keywords
            )
        except Exception as e:
            print(f"ML classification failed: {e}. Falling back to rules.")
            return rule_based_intent_classification(text)
    else:
        # Fallback на правила
        return rule_based_intent_classification(text)


# Функция для обновления модели новыми примерами
def update_intent_model(new_texts: List[str], new_labels: List[int]):
    """Обновление модели новыми примерами"""
    global model
    try:
        if len(new_texts) != len(new_labels):
            raise ValueError("Количество текстов и меток должно совпадать")

        if model is not None:
            # Дообучение модели
            model.fit(new_texts, new_labels)
            joblib.dump(model, model_path)
            return True
        else:
            # Переобучение с нуля
            model = train_intent_model()
            joblib.dump(model, model_path)
            return True
    except Exception as e:
        print(f"Error updating model: {e}")
        return False


# Тестирование
if __name__ == "__main__":
    test_cases = [
        "Создай КС на 300 тысяч",
        "Найди все закупки по ремонту",
        "Покажи мои котировочные сессии",
        "Добавь новую электронную подпись",
        "Что такое котировочная сессия?"
    ]

    for test in test_cases:
        result = classify_intent(test)
        print(f"Текст: {test}")
        print(f"Намерение: {result.intent} (уверенность: {result.confidence:.2f})")
        print(f"Ключевые слова: {result.keywords}")
        print("-" * 50)