# -*- coding: utf-8 -*-
"""Обработчик команды начала диалога с ботом."""

from aiogram.types import Message
from loguru import logger

import config
import text


async def command_authenticate(
    message: Message
) -> None:
    """DOCSTRING."""
    logger.debug("Обработчик:\tcommand_authenticate.")  # Логирование

    password: str = str(message.text).split("/auth", 1)[-1].strip()

    if password == config.PASSWORD:
        config.authenticated.append(message.from_user.id)  # pyright: ignore
        await message.answer(text=text.AUTHENTICATE_2)
        return None
    
    await message.answer(text=text.AUTHENTICATE_3)


async def message_authenticate(
    message: Message
) -> None:
    """Выводит приветственное сообщение."""
    logger.debug("Обработчик:\tmessage_authenticate.")  # Логирование

    await message.answer(text=text.AUTHENTICATE_1)
