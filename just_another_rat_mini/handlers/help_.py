# -*- coding: utf-8 -*-
"""Обработчик, выводящий список команд бота."""

from aiogram.types import Message
from loguru import logger

import text


async def command_help(message: Message) -> None:
    """Выводит список команд с их кратким описанием."""
    logger.debug("Обработчик:\tcommand_help")  # Логирование

    # Выводит справку по команде
    if message.text == "/help /?":
        logger.trace("Вывод справки по команде.")  # Логирование
        await message.answer(text=text.HELP_DOC)
        return None

    await message.answer(text=text.HELP)
