# -*- coding: utf-8 -*-
"""Создаёт и настраивает объекты бота и диспетчера."""

from typing import Final

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from loguru import logger

import config


bot: Bot
dispatcher: Dispatcher


async def init() -> None:
    """Настраивает объекты бота и диспетчера."""
    global bot, dispatcher

    # Базовые настройки бота
    properties: Final = DefaultBotProperties(
        allow_sending_without_reply=False,
        link_preview_prefer_small_media=True,
        parse_mode=config.PARSE_MODE
    )

    # Команды бота в интерфейсе Telegram
    commands: list[BotCommand] = [
        BotCommand(
            command=command,
            description=description
        )
        for command, description in config.BOT_COMMANDS
    ]

    bot = Bot(
        default=properties,
        token=config.BOT_TOKEN
    )
    await bot.set_my_commands(commands=commands)
    logger.trace("Объект бота создан.")  # Логирование

    dispatcher = Dispatcher()
    logger.trace("Объект диспетчера создан.")  # Логирование
