# -*- coding: utf-8 -*-
"""Обработчики загрузки файлов на устройство пользователя."""

from pathlib import Path
from typing import Any, BinaryIO
from aiogram.types import File, Message
from aiogram.fsm.context import FSMContext
from loguru import logger

import bot
import text
from states import GetInput


async def _get_file(message: Message) -> Any:
    """Пытается получить информацию о файле из сообщения администратора.

    Поддерживаемые типы: document, photo, audio, video.

    В случае если тип файла не распознан или файл не был прикреплен вернёт
    None.
    """
    logger.debug("Функция:\t\t_get_file.")  # Логирование

    if message.document:
        logger.info("Тип файла:\t\tДокумент.")  # Логирование
        return message.document

    if message.photo:
        logger.info("Тип файла:\t\tИзображение.")  # Логирование
        return message.photo[-1]

    elif message.audio:
        logger.info("Тип файла:\t\tАудио.")  # Логирование
        return message.audio

    elif message.video:
        logger.info("Тип файла:\t\tВидео.")  # Логирование
        return message.video

    # Логирование
    logger.error("Тип файла не распознан или файл не прикреплен.")
    return None


async def _upload(
    attachment: Any,
    file_name: str,
    message: Message
) -> None:
    """Загружает указанный файл на устройство пользователя.

    В случае, если администратор не указал название файла, будет использовано
    название исходного файла.
    """
    logger.debug("Функция:\t\t_upload.")  # Логирование

    # Администратор не указал название файла
    if not file_name:
        logger.trace(  # Логирование
            "Администратор не указал название файла. "
            "Будет использовано название исходного файла."
        )
        file_name = attachment.file_name

    await message.answer(text=text.UPLOAD_2)

    # Скачивает файл из сообщения администратора
    file: File = await bot.bot.get_file(
        file_id=attachment.file_id
    )
    file_data: BinaryIO | None = await bot.bot.download_file(
        file_path=str(file.file_path)
    )

    # Абсолютный путь к файлу
    file_path: Path = Path(file_name).resolve()

    with open(file=file_path, mode="wb") as fb:
        fb.write(file_data.getvalue())  # pyright: ignore

    await bot.bot.delete_message(
        chat_id=message.from_user.id,  # type: ignore
        message_id=message.message_id + 1
    )

    # Логирование
    logger.success(f"Файл загружен и находится по адресу: '{file_path}'.")

    await message.answer(text=(text.UPLOAD_3 % file_path))


async def command_upload(
    message: Message,
    state: FSMContext
) -> None:
    """Обрабатывает запрос администратора на загрузку файла.

    Если администратор сразу передал файл - получает название файла из
    сообщения и вызывает функцию загрузки. В противном случае настраивает
    машину состояний на запрос файла.
    """
    logger.debug("Обработчик:\tcommand_upload.")  # Логирование

    # Выводит документацию по команде
    if message.text == "/upload /?":
        await message.answer(text=text.DOWNLOAD_DOC)
        logger.trace("Вывод справки по команде.")  # Логирование
        return None

    attachment: Any = await _get_file(message=message)
    if not attachment:
        await state.set_state(GetInput.upload)
        await message.answer(text=text.UPLOAD_1)
        logger.trace("Администратор не передал файл.")  # Логирование
        return None

    file_name: str = str(message.caption).split("/upload", 1)[-1].strip()
    await _upload(
        attachment=attachment,
        file_name=file_name,
        message=message
    )


async def state_upload(
    message: Message,
    state: FSMContext
) -> None:
    """Отключает машину состояний и вызывает функцию загрузки.

    Если администратор передал файл - получает название файла из сообщения
    и вызывает функцию загрузки. В противном случае сообщает администратору
    о ошибке.
    """
    logger.debug("Обработчик:\tstate_upload.")  # Логирование

    await state.clear()

    attachment: Any = await _get_file(message=message)
    if not attachment:
        await message.answer(text=text.UPLOAD_ERR_1)
        logger.trace("Администратор не передал файл.")  # Логирование
        return None

    await _upload(
        attachment=attachment,
        file_name=str(message.caption) if message.caption else "",
        message=message
    )
