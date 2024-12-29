# -*- coding: utf-8 -*-
"""Инструменты для настройки и получения обработчиков бота."""

from aiogram.filters import Command, StateFilter
from loguru import logger

import bot
from filters import IsAuthenticated
from handlers import about, authenticate, download, execute, help_, upload
from states import GetInput


def init() -> None:
    """Настраивает обработчики бота."""

    # /start
    bot.dispatcher.message.register(
        about.command_about,
        Command(commands=["about"]),
        StateFilter(None),
        IsAuthenticated()
    )

    # /download файл
    bot.dispatcher.message.register(
        download.command_download,
        Command(commands=["download"]),
        StateFilter(None),
        IsAuthenticated()
    )

    # /download
    bot.dispatcher.message.register(
        download.state_download,
        StateFilter(GetInput.download),
        IsAuthenticated()
    )

    # /execute команда
    bot.dispatcher.message.register(
        execute.command_execute,
        Command(commands=["execute"]),
        StateFilter(None),
        IsAuthenticated()
    )

    # /execute
    bot.dispatcher.message.register(
        execute.state_execute,
        StateFilter(GetInput.execute),
        IsAuthenticated()
    )

    # /help
    bot.dispatcher.message.register(
        help_.command_help,
        Command(commands=["help"]),
        StateFilter(None),
        IsAuthenticated()
    )

    # /upload file.txt
    bot.dispatcher.message.register(
        upload.command_upload,
        Command(commands=["upload"]),
        StateFilter(None),
        IsAuthenticated()
    )

    # /upload
    bot.dispatcher.message.register(
        upload.state_upload,
        StateFilter(GetInput.upload),
        IsAuthenticated()
    )

    bot.dispatcher.message.register(
        authenticate.command_authenticate,
        Command(commands=["auth"]),
        StateFilter(None),
        ~IsAuthenticated()
    )

    bot.dispatcher.message.register(
        authenticate.message_authenticate,
        StateFilter(None),
        ~IsAuthenticated()
    )

    logger.trace("Обработчики настроены.")  # Логирование
