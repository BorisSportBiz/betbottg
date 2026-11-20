"""
Форматирование поста + наборы кастомных эмодзи под компании.
"""

from typing import Dict, Any

# Кастомные эмодзи (ID из Telegram)
EMOJI_PACKS = {
    "мелбет": {
        "title": "5204103888495455481",
        "player": "5204103888495455481",
        "bookmaker": "5204103888495455481",
        "verdict": "5204103888495455481",
    },
    "фонбет": {
        "title": "5438617705676545736",
        "player": "5438617705676545736",
        "bookmaker": "5438617705676545736",
        "verdict": "5438617705676545736",
    },
    "winline": {
        "title": "5249203579134179981",
        "player": "5249203579134179981",
        "bookmaker": "5249203579134179981",
        "verdict": "5249203579134179981",
    },
    "pari": {
        "title": "5262618295302906003",
        "player": "5262618295302906003",
        "bookmaker": "5262618295302906003",
        "verdict": "5262618295302906003",
    },
    "бетсити": {
        "title": "5393577852522223661",
        "player": "5393577852522223661",
        "bookmaker": "5393577852522223661",
        "verdict": "5393577852522223661",
    },
    "марафон": {
        "title": "5402339843504120923",
        "player": "5402339843504120923",
        "bookmaker": "5402339843504120923",
        "verdict": "5402339843504120923",
    },
    "leon": {
        "title": "5364220239225567667",
        "player": "5364220239225567667",
        "bookmaker": "5364220239225567667",
        "verdict": "5364220239225567667",
    },
    "bettery": {
        "title": "5407055799199492525",
        "player": "5407055799199492525",
        "bookmaker": "5407055799199492525",
        "verdict": "5407055799199492525",
    },
    "лига ставок": {
        "title": "5379914891538743469",
        "player": "5379914891538743469",
        "bookmaker": "5379914891538743469",
        "verdict": "5379914891538743469",
    },
    "betboom": {
        "title": "5395872185397059918",
        "player": "5395872185397059918",
        "bookmaker": "5395872185397059918",
        "verdict": "5395872185397059918",
    },
    "бет-м": {
        "title": "5462938022414679764",
        "player": "5462938022414679764",
        "bookmaker": "5462938022414679764",
        "verdict": "5462938022414679764",
    },
    "зенит": {
        "title": "5381858725017427351",
        "player": "5381858725017427351",
        "bookmaker": "5381858725017427351",
        "verdict": "5381858725017427351",
    },
    "балтбет": {
        "title": "5384537023673540699",
        "player": "5384537023673540699",
        "bookmaker": "5384537023673540699",
        "verdict": "5384537023673540699",
    },
    "24bet": {
        "title": "5296516582384639553",
        "player": "5296516582384639553",
        "bookmaker": "5296516582384639553",
        "verdict": "5296516582384639553",
    },
    "олимп": {
        "title": "5400297492065591585",
        "player": "5400297492065591585",
        "bookmaker": "5400297492065591585",
        "verdict": "5400297492065591585",
    },
    "default": {
        "title": "📢",
        "player": "👤",
        "bookmaker": "🏢",
        "verdict": "✅",
    },
}

COMPANY_KEYWORDS = {
    "мелбет": ["мелбет", "melbet"],
    "фонбет": ["фонбет", "fonbet"],
    "winline": ["winline", "винлайн"],
    "pari": ["pari", "пари"],
    "бетсити": ["бетсити", "betcity"],
    "марафон": ["марафон", "марафонбет", "marathon"],
    "leon": ["leon", "леон"],
    "bettery": ["bettery", "беттери"],
    "лига ставок": ["лига ставок", "ligastavok"],
    "betboom": ["betboom", "бетбум"],
    "бет-м": ["бет-м", "bet-m"],
    "зенит": ["зенит", "zenit"],
    "балтбет": ["балтбет", "baltbet"],
    "24bet": ["24bet"],
    "олимп": ["олимп", "olimpbet", "olimp"],
}


def detect_company(text: str) -> str:
    text_lower = text.lower()
    for company, keywords in COMPANY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return company
    return "default"


def emoji_tag(emoji_id: str, fallback: str = "🎁") -> str:
    if emoji_id.isdigit():
        return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
    return emoji_id


def get_emoji_pack(company: str) -> Dict[str, str]:
    key = company.lower().strip()
    return EMOJI_PACKS.get(key, EMOJI_PACKS["default"])


def format_post(analysis: Dict[str, Any]) -> str:
    raw_text = analysis.get("raw", "") + " " + analysis.get("title", "")
    company = analysis.get("company") or detect_company(raw_text)
    if company in ("Букмекер", "Неизвестно", "default"):
        company = detect_company(raw_text)

    emojis = get_emoji_pack(company)

    title_emoji = emoji_tag(emojis["title"])
    player_emoji = emoji_tag(emojis["player"])
    bookmaker_emoji = emoji_tag(emojis["bookmaker"])
    verdict_emoji = emoji_tag(emojis["verdict"])

    title = analysis.get("title", f"{company.capitalize()} запускает акцию")
    essence = analysis.get("essence", "—")
    deadline = analysis.get("deadline", "не указано")
    prizes = analysis.get("prizes_count", "не указано")
    important = analysis.get("important", "смотри полные правила")
    for_player = analysis.get("for_player", "—")
    for_bookmaker = analysis.get("for_bookmaker", "—")
    verdict = analysis.get("verdict", "—")

    post = f"""{title_emoji} <b>{title}</b>

<b>Суть акции:</b> {essence}

<b>Сроки акции:</b> {deadline}

<b>Количество призов:</b> {prizes}

<b>Важно:</b> {important}

{player_emoji} <b>Для игрока:</b>
{for_player}

{bookmaker_emoji} <b>Для букмекера:</b>
{for_bookmaker}

{verdict_emoji} <b>Вердикт «Акции вверх!»:</b>
{verdict}"""

    return post
