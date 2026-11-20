"""
Telegram-бот для генерации постов-разборов акций.
Принимает текст / PDF / DOCX / Google Doc → выдаёт готовый пост.
"""

import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from analyzer import analyze_promo
from extractors import extract_text_from_message
from templates import format_post

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Временное хранилище последних текстов (для простоты, потом можно заменить на FSM)
user_texts: dict[int, str] = {}


@dp.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Доступ только для владельца.")
        return
    await message.answer(
        "Привет. Кидай текст акции, PDF, DOCX или ссылку на Google Doc — "
        "сделаю готовый пост в твоём стандарте."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(
        "Как пользоваться:\n"
        "1. Отправь текст / файл / ссылку\n"
        "2. Напиши /post или просто «сделай пост»\n"
        "3. Получишь готовый разбор с эмодзи под компанию"
    )


@dp.message(F.document | F.text)
async def handle_input(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("Получил. Извлекаю текст...")

    try:
        text = await extract_text_from_message(message, bot)
        if not text or len(text) < 50:
            await message.answer("Не удалось извлечь достаточно текста.")
            return

        user_texts[message.from_user.id] = text
        await message.answer(
            f"Текст извлечён ({len(text)} символов).\n"
            "Напиши /post чтобы сгенерировать разбор."
        )
    except Exception as e:
        logger.exception("Ошибка извлечения")
        await message.answer(f"Ошибка при извлечении текста: {e}")


@dp.message(Command("post"))
async def cmd_post(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = user_texts.get(message.from_user.id)
    if not text:
        await message.answer("Сначала отправь текст или файл.")
        return

    await message.answer("Готовлю пост...")

    try:
        analysis = await analyze_promo(text)
        post = format_post(analysis)
        await message.answer(post, parse_mode=ParseMode.HTML)
        await message.answer(
            "Пост выше — шаблон.\n"
            "Можешь скопировать и дописать нужные блоки вручную "
            "или прислать мне готовые формулировки."
        )
    except Exception as e:
        logger.exception("Ошибка анализа")
        await message.answer(f"Ошибка при генерации поста: {e}")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан")
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
