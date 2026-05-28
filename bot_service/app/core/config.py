# bot_service/app/core/config.py

"""
Конфигурация Bot Service.

Здесь:
- читаются переменные окружения из .env
- хранятся настройки Telegram-бота
- настраиваются JWT параметры
- настраиваются Redis и RabbitMQ
- настраивается OpenRouter API

Файл НЕ:
- запускает FastAPI
- запускает aiogram
- выполняет HTTP-запросы
- работает с Redis напрямую
"""

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Глобальные настройки Bot Service.

    Значения автоматически читаются:
    - из переменных окружения
    - из .env файла
    """

    # Название приложения
    app_name: str = "bot-service"

    # Окружение
    # local / dev / prod
    env: str = "local"

    # Telegram Bot Token
    telegram_bot_token: str

    # URL Auth Service
    auth_service_url: str = "http://auth_service:8000"

    # JWT настройки
    jwt_secret: str = "change_me_super_secret"
    jwt_alg: str = "HS256"

    # Redis
    # Для docker-compose используем redis,
    # а не localhost
    redis_url: str = "redis://redis:6379/0"

    # RabbitMQ
    # Для docker-compose используем rabbitmq
    rabbitmq_url: str = (
        "amqp://guest:guest@rabbitmq:5672//"
    )

    # OpenRouter API
    openrouter_api_key: str = ""

    openrouter_base_url: str = (
        "https://openrouter.ai/api/v1"
    )

    openrouter_model: str = (
        "stepfun/step-3.5-flash:free"
    )

    openrouter_site_url: str = (
        "https://example.com"
    )

    openrouter_app_name: str = "bot-service"

    # Настройки pydantic-settings
    model_config = SettingsConfigDict(

        # Путь к .env
        env_file=".env",

        # Кодировка
        env_file_encoding="utf-8",

        # Игнорировать лишние поля
        extra="ignore",
    )


# Глобальный объект настроек
settings = Settings()