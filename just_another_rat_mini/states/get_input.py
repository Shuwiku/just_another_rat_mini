# -*- coding: utf-8 -*-
"""Машина состояний запроса ввода."""

from aiogram.fsm.state import State, StatesGroup


class GetInput(StatesGroup):
    """Машина состояний запроса ввода."""

    download: State = State()
    execute: State = State()
    password: State = State()
    upload: State = State()
