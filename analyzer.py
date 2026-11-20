"""
Анализ акции — режим без API (только форматирование).
"""

from typing import Dict, Any
from templates import detect_company


async def analyze_promo(text: str) -> Dict[str, Any]:
    """
    Без API: возвращает структуру с заглушками.
    Пользователь сам заполняет ключевые блоки в чате.
    """
    company = detect_company(text)

    return {
        "company": company,
        "title": f"{company.capitalize()} запускает акцию",
        "essence": "Смотри условия в тексте выше.",
        "deadline": "уточняется",
        "prizes_count": "смотри правила",
        "important": "смотри полные правила акции",
        "for_player": "Низкий порог входа. Реальный шанс зависит от количества участников.",
        "for_bookmaker": "Маркетинговые расходы контролируемые, взамен — дополнительный оборот и лояльность.",
        "verdict": "Обычная акция на удержание и активность.",
        "raw": text[:500],
    }
