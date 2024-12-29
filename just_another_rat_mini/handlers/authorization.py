# -*- coding: utf-8 -*-
"""Обработчики авторизации в боте."""

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

import config
import text
from states import GetInput


async def _authorization(
    message: Message,
    password: str
) -> None:
    """Проверяет переданный пароль на соответствие с паролем в конфигурации.

    Если пароли совпадают - добавляет администратора в список авторизованных и
    отправляет сообщение с информацией о боте.
    """
    logger.debug("Функция:\t\t_authorization.")  # Логирование

    # Переданный пароль и пароль из конфигурации совпадают
    if password == config.PASSWORD:
        await message.answer(text=text.AUTHORIZATION_2)
        await message.answer(text=text.ABOUT)
        config.authenticated.append(message.from_user.id)  # pyright: ignore
        logger.info("Администратор прошёл авторизацию.")  # Логирование
        return None

    # Пароли не совпали
    await message.answer(text=text.AUTHORIZATION_3)
    logger.warning("Администратор не прошёл авторизацию!")  # Логирование


async def command_authorization(
    message: Message,
    state: FSMContext
) -> None:
    """Обрабатывает запрос администратора на авторизацию.

    Если администратор передал пароль - вызывает функцию авторизации. В
    противном случае настраивает машину состояний на запрос пароля.
    """
    logger.debug("Обработчик:\tcommand_authorization.")  # Логирование

    # Выводит документацию по команде
    if message.text == "/auth /?":
        logger.trace("Вывод справки по команде.")  # Логирование
        await message.answer(text=text.AUTHORIZATION_DOC)
        return None

    # Пароль для авторизации
    password: str = str(message.text).split("/auth", 1)[-1].strip()

    # Администратор не указал пароль (ввод "/auth")
    if not password:
        await state.set_state(GetInput.password)
        await message.answer(text=text.AUTHORIZATION_4)
        logger.trace("Администратор не указал пароль.")  # Логирование
        return None

    await _authorization(
        message=message,
        password=password
    )


async def message_authorization(message: Message) -> None:
    """Выводит сообщение с указанием авторизоваться в боте."""
    logger.debug("Обработчик:\tmessage_authorization.")  # Логирование

    await message.answer(text=text.AUTHORIZATION_1)


async def state_authorization(
    message: Message,
    state: FSMContext
) -> None:
    """Отключает машину состояний и вызывает функцию авторизации."""
    logger.debug("Обработчик:\tstate_authorization.")  # Логирование

    await state.clear()

    await _authorization(
        message=message,
        password=str(message.text).strip()
    )
