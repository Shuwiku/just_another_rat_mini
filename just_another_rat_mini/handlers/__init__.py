# -*- coding: utf-8 -*-
"""Функция регистрации обработчиков в диспетчере."""

from aiogram.filters import Command, StateFilter
from loguru import logger

import bot
from filters import IsAuthenticated
from handlers import about, authorization, download, execute, help_, upload
from states import GetInput


def init() -> None:
    """Регистрирует обработчики в диспетчере."""

    # /about
    bot.dispatcher.message.register(
        about.command_about,
        Command(commands=["about"]),
        StateFilter(None),
        IsAuthenticated()
    )

    # /download file.txt
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

    # /execute command
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

    # /auth password
    bot.dispatcher.message.register(
        authorization.command_authorization,
        Command(commands=["auth"]),
        StateFilter(None),
        ~IsAuthenticated()
    )

    # Любое сообщение до того, как администратор прошёл аутентификацию
    bot.dispatcher.message.register(
        authorization.message_authorization,
        StateFilter(None),
        ~IsAuthenticated()
    )

    # /auth
    bot.dispatcher.message.register(
        authorization.state_authorization,
        StateFilter(GetInput.password),
        ~IsAuthenticated()
    )

    logger.trace("Обработчики зарегистрированы.")  # Логирование
