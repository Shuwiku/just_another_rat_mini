# -*- coding: utf-8 -*-
"""DOCSTRING."""

from aiogram.filters import Filter
from aiogram.types import Message

from loguru import logger

import config


class IsAuthenticated(Filter):
    """DOCSTRING."""
    
    async def __call__(
        self,
        message: Message
    ) -> bool:
        """DOCSTRING."""
        logger.debug("Фильтр:\t\tIsAuthenticated")  # Логирование
        if message.from_user.id in config.authenticated:  # pyright: ignore
            return True
        return False
