# bot_service/app/tasks/llm_tasks.py

"""
Celery-задачи для LLM-запросов Bot Service.

Здесь:
- описывается задача llm_request
- вызывается OpenRouter API
- формируется ответ пользователю
- сообщение отправляется обратно в Telegram

Файл НЕ:
- проверяет JWT
- хранит пользователей
- содержит aiogram handlers
"""

import asyncio

# Telegram Bot из aiogram
from aiogram import Bot

# Настройки приложения
from app.core.config import settings

# Celery-приложение
from app.infra.celery_app import celery_app

# Клиент OpenRouter
from app.services.openrouter_client import call_openrouter


@celery_app.task(name="llm_request")
def llm_request(
    tg_chat_id: int,
    prompt: str,
) -> None:
    """
    Celery-задача обработки LLM-запроса.

    Шаги:
    1. Получает chat_id пользователя Telegram.
    2. Получает текстовый запрос prompt.
    3. Вызывает OpenRouter API.
    4. Отправляет ответ пользователю в Telegram.
    """

    asyncio.run(
        _process_llm_request(
            tg_chat_id=tg_chat_id,
            prompt=prompt,
        )
    )


async def _process_llm_request(
    tg_chat_id: int,
    prompt: str,
) -> None:
    """
    Асинхронная часть Celery-задачи.

    Нужна, потому что:
    - OpenRouter вызывается через async httpx
    - aiogram Bot тоже работает асинхронно
    """

    bot = Bot(token=settings.telegram_bot_token)

    try:
        # Запрос к LLM через OpenRouter
        answer = await call_openrouter(prompt)

        # Отправка ответа пользователю
        await bot.send_message(
            chat_id=tg_chat_id,
            text=answer,
        )

    except Exception as exc:
        # Сообщение пользователю при ошибке
        await bot.send_message(
            chat_id=tg_chat_id,
            text=("Произошла ошибка при обработке LLM-запроса. Попробуйте позже."),
        )

        # Пробрасываем ошибку дальше,
        # чтобы Celery отметил задачу как failed
        raise exc

    finally:
        # Закрываем HTTP-сессию бота
        await bot.session.close()
