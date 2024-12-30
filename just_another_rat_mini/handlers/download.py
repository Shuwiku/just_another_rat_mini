# -*- coding: utf-8 -*-
"""Обработчики загрузки файлов с устройства пользователя."""

from pathlib import Path

from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from loguru import logger

import bot
import text
from states import GetInput


async def _download(
    file_name: str,
    message: Message
) -> None:
    """Загружает указанный файл и отправляет его администратору.

    В случае, если файл по указанному пути не существует или соединение
    пользователя с Интернетом слишком слабое (такое, что не получается
    отправить файл), уведомит об этом администратора.
    """
    logger.debug("Функция:\t\t_download.")  # Логирование

    # Абсолютный путь к файлу
    file_path: Path = Path(file_name).resolve()

    # Файл не существует
    if not file_path.is_file():
        await message.answer(text=(text.DOWNLOAD_ERR_1 % file_path))
        logger.error(f"Файл не найден: '{file_path}'.")  # Логирование
        return None

    # Временное сообщение
    await message.answer(text=text.DOWNLOAD_2)
    logger.info(f"Отправляю файл: '{file_path}'.")  # Логирование

    try:  # Отправляет файл
        await message.answer_document(
            document=FSInputFile(path=file_path),
            caption=text.DOWNLOAD_3
        )
        logger.success("Файл успешно отправлен администратору.")  # Логирование

    # Время ожидания сервером передачи истекло
    except TelegramNetworkError as e:
        await message.answer(text=text.DOWNLOAD_ERR_2)
        logger.error(e)  # Логирование

    # Непредвиденная ошибка
    except Exception as e:
        await message.answer(text=(text.DOWNLOAD_ERR_3 % e))
        logger.error(e)  # Логирование

    # Удаляет временное сообщение
    await bot.bot.delete_message(
        chat_id=message.from_user.id,  # type: ignore
        message_id=message.message_id + 1
    )


async def command_download(
    message: Message,
    state: FSMContext
) -> None:
    """Обрабатывает запрос администратора на скачивание файла.

    Если администратор сразу передал название или путь к файлу - вызывает
    функцию загрузки. В противном случае настраивает машину состояний на
    запрос названия файла.
    """
    logger.debug("Обработчик:\tcommand_download.")  # Логирование

    # Выводит документацию по команде
    if message.text == "/download /?":
        await message.answer(text=text.DOWNLOAD_DOC)
        logger.trace("Вывод справки по команде.")  # Логирование
        return None

    # Название файла
    file_name: str = str(message.text).split("/download", 1)[-1].strip()

    # Администратор не указал название файла (ввод "/download")
    if not file_name:  # Переводит в обработчик state_download
        await state.set_state(GetInput.download)
        await message.answer(text=text.DOWNLOAD_1)
        logger.trace("Администратор не указал название файла.")  # Логирование
        return None

    await _download(
        file_name=file_name,
        message=message
    )


async def state_download(
    message: Message,
    state: FSMContext
) -> None:
    """Отключает машину состояний и вызывает функцию загрузки."""
    logger.debug("Обработчик:\tstate_download.")  # Логирование

    await state.clear()

    await _download(
        file_name=str(message.text).strip(),
        message=message
    )
