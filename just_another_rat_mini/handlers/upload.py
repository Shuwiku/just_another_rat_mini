# -*- coding: utf-8 -*-
"""Загружает файл, отправленный администратором на устройство пользователя."""

from pathlib import Path
from typing import Any, BinaryIO
from aiogram.types import File, Message
from aiogram.fsm.context import FSMContext
from loguru import logger

import bot
import text
from states import GetInput


async def _get_file(message: Message) -> Any:
    """Получает файл из сообщения администратора."""
    logger.debug("Функция:\t\t_get_file.")  # Логирование

    if message.document:
        logger.trace("Тип файла:\t\tДокумент.")  # Логирование
        return message.document

    if message.photo:
        logger.trace("Тип файла:\t\tИзображение.")  # Логирование
        return message.photo[-1]

    elif message.audio:
        logger.trace("Тип файла:\t\tАудио.")  # Логирование
        return message.audio

    elif message.video:
        logger.trace("Тип файла:\t\tВидео.")  # Логирование
        return message.video

    # Логирование
    logger.error("Тип файла не распознан или файл не прикреплен.")
    return None


async def _upload(
    attachment: Any,
    file_name: str,
    message: Message
) -> None:
    """Загружает файл на устройство пользователя."""
    logger.debug("Функция:\t\t_upload.")  # Логирование

    if not file_name:
        logger.trace(  # Логирование
            "Администратор не указал название файла. "
            "Будет использовано название исходного файла."
        )
        file_name = attachment.file_name

    file_path: Path = Path(file_name).resolve()

    file: File = await bot.bot.get_file(
        file_id=attachment.file_id
    )

    await message.answer(text=text.UPLOAD_2)
    file_data: BinaryIO | None = await bot.bot.download_file(
        file_path=str(file.file_path)
    )

    with open(file=file_path, mode="wb") as fb:
        fb.write(file_data.getvalue())  # pyright: ignore

    await bot.bot.delete_message(
        chat_id=message.from_user.id,  # type: ignore
        message_id=message.message_id + 1
    )

    # Логирование
    logger.trace(f"Файл загружен и находится по адресу: '{file_path}'.")

    await message.answer(text=(text.UPLOAD_3 % file_path))


async def command_upload(
    message: Message,
    state: FSMContext
) -> None:
    """Загружает файл на устройство пользователя."""
    logger.debug("Обработчик:\tcommand_upload.")  # Логирование

    # Выводит документацию по команде
    if message.text == "/upload /?":
        logger.trace("Вывод справки по команде.")  # Логирование
        await message.answer(text=text.DOWNLOAD_DOC)
        return None

    attachment: Any = await _get_file(message=message)
    if not attachment:
        logger.trace("Администратор не передал файл.")  # Логирование
        await state.set_state(GetInput.upload)
        await message.answer(text=text.UPLOAD_1)
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
    """Загружает файл на устройство пользователя."""
    logger.debug("Обработчик:\tstate_upload.")  # Логирование

    attachment: Any = await _get_file(message=message)
    if not attachment:
        logger.trace("Администратор не передал файл.")  # Логирование
        await state.clear()
        await message.answer(text=text.UPLOAD_ERR_1)
        return None

    await state.clear()
    await _upload(
        attachment=attachment,
        file_name=str(message.caption) if message.caption else "",
        message=message
    )
