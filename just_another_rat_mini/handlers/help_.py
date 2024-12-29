# -*- coding: utf-8 -*-
"""Выводит список команд с их кратким описанием."""

from aiogram.types import Message
from loguru import logger

import text


async def command_help(message: Message) -> None:
    """Выводит список команд с их кратким описанием."""
    logger.debug("Обработчик:\tcommand_help")  # Логирование

    # Выводит справку по команде
    if message.text == "/help /?":
        await message.answer(text=text.HELP_DOC)
        return None

    await message.answer(text=text.HELP)
