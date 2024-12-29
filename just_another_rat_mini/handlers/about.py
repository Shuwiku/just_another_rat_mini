# -*- coding: utf-8 -*-
"""Обработчик команды начала диалога с ботом."""

from aiogram.types import Message
from loguru import logger

import text


async def command_about(message: Message) -> None:
    """Выводит приветственное сообщение."""
    logger.debug("Обработчик:\tcommand_start")  # Логирование

    # Выводит документацию по команде
    if message.text == "/about /?":
        logger.trace("Вывод справки по команде.")  # Логирование
        await message.answer(text=text.START_DOC)
        return None

    await message.answer(text=text.START)
