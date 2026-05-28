# bot_service/app/infra/celery_app.py

"""
Celery-конфигурация Bot Service.

Здесь:
- создаётся celery_app
- настраивается RabbitMQ broker
- настраивается Redis backend
- регистрируются Celery tasks

Файл НЕ:
- содержит Telegram bot handlers
- содержит aiogram логику
- выполняет запросы к LLM напрямую
"""

# Celery task queue
from celery import Celery

# Настройки приложения
from app.core.config import settings


# Создание Celery приложения
celery_app = Celery(

    # Имя приложения
    "bot_service",

    # RabbitMQ broker
    broker=settings.rabbitmq_url,

    # Redis backend
    backend=settings.redis_url,
)


# Конфигурация Celery
celery_app.conf.update(

    # Сериализация задач
    task_serializer="json",

    # Сериализация результатов
    result_serializer="json",

    # Формат сообщений
    accept_content=["json"],

    # UTC timezone
    timezone="UTC",

    # Использовать UTC
    enable_utc=True,
)


# Автоматический поиск tasks
# ВАЖНО:
# Без этого Celery может не найти llm_request
# и появится ошибка KeyError
celery_app.autodiscover_tasks(
    ["app.tasks"]
)


# Дополнительно можно импортировать tasks явно
# для гарантированной регистрации
import app.tasks.llm_tasks  # noqa