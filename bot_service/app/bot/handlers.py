# bot_service/app/bot/handlers.py

"""
Telegram-handlers Bot Service.

Здесь:
- обрабатывается команда /token <jwt>
- JWT сохраняется в Redis по Telegram user_id
- обычные сообщения проверяются на наличие JWT
- JWT валидируется локально
- LLM-запрос отправляется в Celery через llm_request.delay(...)
- пользователь получает уведомление о принятии запроса

Файл НЕ:
- создаёт JWT
- обращается к базе Auth Service
- вызывает OpenRouter напрямую
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

# Проверка JWT
from app.core.jwt import decode_and_validate

# Redis-клиент
from app.infra.redis import get_redis

# Celery-задача LLM
from app.tasks.llm_tasks import llm_request


# Router для Telegram handlers
router = Router()


@router.message(Command("token"))
async def token_handler(message: Message) -> None:
    """
    Обработчик команды:
    /token <jwt>
    """

    if message.from_user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    parts = (message.text or "").split(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Передайте токен в формате:\n"
            "/token <jwt>"
        )
        return

    token = parts[1].strip()

    try:
        decode_and_validate(token)

    except ValueError:
        await message.answer(
            "Токен неверный или истёк. "
            "Получите новый токен в Auth Service."
        )
        return

    redis = get_redis()

    key = f"token:{message.from_user.id}"

    await redis.set(
        key,
        token,
    )

    await message.answer("Токен принят и сохранён.")


@router.message()
async def text_handler(message: Message) -> None:
    """
    Обработчик обычного текста.

    Проверяет JWT и отправляет LLM-запрос в Celery.
    """

    if message.from_user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    redis = get_redis()

    key = f"token:{message.from_user.id}"

    token = await redis.get(key)

    if not token:
        await message.answer(
            "Доступ запрещён. Сначала авторизуйтесь:\n"
            "/token <jwt>"
        )
        return

    try:
        decode_and_validate(token)

    except ValueError:
        await message.answer(
            "Токен недействителен или истёк. "
            "Получите новый токен в Auth Service "
            "и отправьте командой /token <jwt>."
        )
        return

    llm_request.delay(
        tg_chat_id=message.chat.id,
        prompt=message.text or "",
    )

    await message.answer(
        "Запрос принят. Ответ придёт после обработки."
    )