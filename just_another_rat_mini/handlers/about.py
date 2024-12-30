# -*- coding: utf-8 -*-
"""Обработчик, выводящий информацию о утилите."""

from aiogram.types import Message
from loguru import logger

import text


async def command_about(message: Message) -> None:
    """Выводит информацию о утилите."""
    logger.debug("Обработчик:\tcommand_about.")  # Логирование

    # Выводит документацию по команде
    if message.text == "/about /?":
        await message.answer(text=text.ABOUT_DOC)
        logger.trace("Вывод справки по команде.")  # Логирование
        return None

    await message.answer(text=text.ABOUT)
