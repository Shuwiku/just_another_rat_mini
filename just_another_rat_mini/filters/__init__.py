# -*- coding: utf-8 -*-
"""Фильтры aiogram для обработчиков бота."""

# Это позволяет импортировать классы напрямую из модуля
# Вместо:   from filters.is_authenticated import IsAuthenticated
# Будет:    from filters import IsAuthenticated
from .is_authenticated import IsAuthenticated  # noqa: F401
