# bot_service/app/bot/dispatcher.py

"""
Создание Telegram Bot и Dispatcher.

Здесь:
- создаётся Bot
- создаётся Dispatcher
- подключаются handlers

Файл НЕ содержит:
- бизнес-логику
- JWT-проверку
- Redis
- Celery
"""

from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.bot.handlers import router


# Создание Telegram Bot
bot = Bot(token=settings.telegram_bot_token)

# Создание Dispatcher
dp = Dispatcher()

# Подключение handlers
dp.include_router(router)