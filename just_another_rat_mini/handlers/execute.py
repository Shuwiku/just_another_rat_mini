# -*- coding: utf-8 -*-
"""Выполняет переданную команду и отправляет результат её выполнения."""

import os
import subprocess

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

import text
from states import GetInput


async def _execute(
    command: str,
    message: Message
) -> None:
    """Выполняет переданную команду и отправляет результат её выполения."""
    logger.debug("Функция:\t\t_execute")  # Логирование

    logger.trace(f"Выполнение команды: '{command}'.")  # Логирование

    # Иное поведение для команды "cd"
    if command == "cd" or command.startswith("cd "):
        return await _execute_cd(
            command=command,
            message=message
        )

    try:  # Пытается выполнить переданную команду
        result: str = subprocess.check_output(
            args=["cmd", "/c", command],
            encoding="cp866"
        ).strip()

        logger.trace("Команда успешно выполнена.")  # Логирование

        # Команда вернула результат своей работы
        if result:
            await message.answer(text=(text.EXECUTE_2 % result))
            return None

        await message.answer(text=text.EXECUTE_3)

    # Ошибка при выполнении команды
    except subprocess.CalledProcessError as e:
        await message.answer(text=(text.EXECUTE_ERR_1 % e))
        logger.error(e)  # Логирование

    # Непредвиденная ошибка
    except Exception as e:
        await message.answer(text=(text.EXECUTE_ERR_2 % e))
        logger.error(e)  # Логирование


async def _execute_cd(
    command: str,
    message: Message
) -> None:
    """Выполняет команду "cd" и отправляет результат её выполения."""
    logger.debug("Функция:\t\t_execute_cd")  # Логирование

    # Команда "cd" без аргументов
    if command == "cd":
        await message.answer(text=(text.EXECUTE_CD_1 % os.getcwd()))
        logger.info("Вывожу текущую директорию.")  # Логирование
        return None

    # Пытается сменить рабочую директорию на указанную
    try:
        # Директория, переданная администратором
        directory: str = command.split("cd", 1)[-1].strip()

        os.chdir(directory)

        await message.answer(text=(text.EXECUTE_CD_2 % os.getcwd()))

        # Логирование
        logger.info(f"Рабочая директория изменена на: '{os.getcwd()}'.")

    # Указанной директории не существует
    except FileNotFoundError as e:
        await message.answer(text=text.EXECUTE_ERR_CD_1)
        logger.error(e)  # Логирование

    # По указанному пути находится файл, а не директория
    except NotADirectoryError as e:
        await message.answer(text=text.EXECUTE_ERR_CD_2)
        logger.error(e)  # Логирование

    # К указанной директории нет доступа
    except PermissionError as e:
        await message.answer(text=text.EXECUTE_ERR_CD_3)
        logger.error(e)  # Логирование

    # Непредвиденная ошибка
    except Exception as e:
        await message.answer(text=(text.EXECUTE_ERR_CD_4 % e))
        logger.error(e)  # Логирование


async def command_execute(
    message: Message,
    state: FSMContext
) -> None:
    """Выполняет переданную команду и отправляет результат её выполения.

    Если команда не была передана - запускает машину состояний и запрашивает
    ввод команды.
    """
    logger.debug("Обработчик:\tcommand_execute.")  # Логирование

    # Выводит документацию по команде
    if message.text == "/execute /?":
        await message.answer(text=text.EXECUTE_DOC)
        logger.trace("Вывод справки по команде.")  # Логирование
        return None

    # Команда, переданная администратором
    command: str = str(message.text).split("/execute", 1)[-1].strip()

    # Администратор не передал команду (ввод "/execute")
    if not command:
        await state.set_state(GetInput.execute)
        await message.answer(text=text.EXECUTE_1)
        logger.trace("Администратор не передал команду.")  # Логирование
        return None

    await _execute(
        command=command,
        message=message
    )


async def state_execute(
    message: Message,
    state: FSMContext
) -> None:
    """Выполняет переданную команду и отправляет результат её выполения."""
    logger.debug("Обработчик:\tstate_execute.")  # Логирование

    await state.clear()

    await _execute(
        command=str(message.text).strip(),
        message=message
    )
