# -*- coding: utf-8 -*-
"""Фильтр, проверяющий доступ администратора к функционалу бота."""

from aiogram.filters import Filter
from aiogram.types import Message

from loguru import logger

import config


class IsAuthenticated(Filter):
    """Фильтр, проверяющий доступ администратора к функционалу бота."""

    async def __call__(
        self,
        message: Message
    ) -> bool:
        """Проверяет доступ администратора к функционалу бота.

        Returns:
            bool: True, если администратор прошёл аутентификацию
                (ID администратора есть в списке). В противном случае False.
        """
        logger.debug("Фильтр:\t\tIsAuthenticated")  # Логирование

        # ID администратора есть в списке
        if message.from_user.id in config.authenticated:  # pyright: ignore
            return True

        return False
