"""
Telegram-бот только для форматирования уже готовых постов.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from templates import format_post, detect_company

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    if ADMIN_ID and message.from_user.id != ADMIN_ID:
        await message.answer("Доступ только для владельца.")
        return
    await message.answer(
        "Привет. Кидай готовый текст поста — я отформатирую его "
        "и подставлю кастомные эмодзи под букмекера."
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    if ADMIN_ID and message.from_user.id != ADMIN_ID:
        return
    await message.answer(
        "Как пользоваться:\n"
        "1. Скопируй готовый текст поста из чата\n"
        "2. Отправь его мне\n"
        "3. Получишь отформатированный пост с эмодзи"
    )


@dp.message(F.text)
async def handle_text(message: Message):
    if ADMIN_ID and message.from_user.id != ADMIN_ID:
        return

    text = message.text.strip()
    if len(text) < 20:
        await message.answer("Слишком короткий текст.")
        return

    analysis = {
        "company": detect_company(text),
        "title": text.split("\n")[0][:100],
        "essence": "—",
        "deadline": "—",
        "prizes_count": "—",
        "important": "—",
        "for_player": text,
        "for_bookmaker": "",
        "verdict": "",
        "raw": text,
    }

    try:
        post = format_post(analysis)
        await message.answer(post, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.exception("Ошибка форматирования")
        await message.answer(f"Ошибка: {e}")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не задан в .env")
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
