"""
Извлечение текста из разных источников.
"""

import io
import re
from pathlib import Path

import pdfplumber
from docx import Document
from aiogram.types import Message
from aiogram import Bot


async def extract_text_from_message(message: Message, bot: Bot) -> str:
    # Простой текст
    if message.text and not message.text.startswith("/"):
        return message.text.strip()

    # Документ
    if message.document:
        file = await bot.get_file(message.document.file_id)
        file_bytes = await bot.download_file(file.file_path)
        content = file_bytes.read()

        filename = message.document.file_name or ""
        if filename.lower().endswith(".pdf"):
            return extract_pdf(content)
        elif filename.lower().endswith((".docx", ".doc")):
            return extract_docx(content)
        else:
            # Пытаемся как текст
            try:
                return content.decode("utf-8", errors="ignore")
            except Exception:
                return ""

    return ""


def extract_pdf(content: bytes) -> str:
    text_parts = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts).strip()


def extract_docx(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_google_doc(url: str) -> str:
    """
    Пока заглушка. Для полноценной работы нужен Google Docs API + credentials.
    Можно попросить пользователя экспортировать в PDF/текст или открыть доступ по ссылке.
    """
    # TODO: реализовать через Google API
    return ""
