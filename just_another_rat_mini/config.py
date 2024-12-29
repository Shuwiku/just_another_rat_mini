# -*- coding: utf-8 -*-
"""Конфигурация бота."""

from pathlib import Path


_bot_dir: Path = Path(".").resolve()

# Настройки бота
BOT_COMMANDS: list[list[str]] = [
    [
        "download",
        "📄 Скачать файл с устройства пользователя."
    ],
    [
        "execute",
        "💻 Выполнить переданную команду."
    ],
    [
        "help",
        "⚙️ Вывести список команд бота."
    ],
    [
        "about",
        "⚙️ Вывести информацию о боте."
    ],
    [
        "upload",
        "📄 Загрузить файл на устройство пользователя."
    ]
]
BOT_TOKEN: str = "BOT_TOKEN_HERE"
PARSE_MODE: str = "Markdown"

# Логирование
LOG_FILES_PATH: str = str(_bot_dir / "logs.log")
LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> |" \
                  " <level>{level: <8}</level> | <level>{message}</level>"
LOG_LEVEL: str = "TRACE"

# Уведомить ли администратора при запуске бота
ADMIN_ID: int = 0
NOTIFY_ON_STARTUP: bool = True

# Защита от посторонних
authenticated: list[int] = []
PASSWORD: str = "password"
