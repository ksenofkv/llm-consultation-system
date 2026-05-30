# bot_service/app/bot/run_polling.py

"""
Entrypoint запуска Telegram-бота.

Здесь:
- запускается aiogram polling
- используется Dispatcher
- подключается Bot
- бот начинает слушать Telegram updates

Файл НЕ:
- содержит handlers
- проверяет JWT
- вызывает OpenRouter
- создаёт Celery tasks
"""

import asyncio

# Bot и Dispatcher
from app.bot.dispatcher import (
    bot,
    dp,
)


async def main() -> None:
    """
    Главная функция запуска polling.
    """

    # Запуск Telegram polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Запуск async приложения
    asyncio.run(main())
