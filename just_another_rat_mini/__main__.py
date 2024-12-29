# -*- coding: utf-8 -*-
"""Just Another Rat."""

import asyncio
import sys

from loguru import logger

import bot
import config
import handlers
import text


async def main() -> None:
    """If __name__ == "__main__"."""
    # Настройка логирования
    logger.remove()

    if sys.stdout is not None:

        logger.add(
            sink=sys.stdout,
            level=config.LOG_LEVEL,
            format=config.LOG_FORMAT
        )

    logger.add(
        sink=config.LOG_FILES_PATH,
        level=config.LOG_LEVEL,
        format=config.LOG_FORMAT
    )

    logger.trace("Логирование настроено.")  # Логирование

    await bot.init()
    handlers.init()

    if config.NOTIFY_ON_STARTUP:
        logger.info("Отправляю сообщение администратору о запуске утилиты.")
        try:
            await bot.bot.send_message(
                chat_id=config.ADMIN_ID,
                text=text.NOTIFY_ON_STARTUP
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение: {e}")

    logger.info("Запуск диспетчера.")  # Логирование

    await bot.dispatcher.start_polling(
        bot.bot,
        skip_updates=True
    )


if __name__ == "__main__":
    asyncio.set_event_loop_policy(
        policy=asyncio.WindowsSelectorEventLoopPolicy()
    )
    asyncio.run(main())
