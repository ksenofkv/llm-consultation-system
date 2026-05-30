# auth_service/app/core/config.py
"""
Файл конфигурации Auth Service.

Здесь:
- читаются переменные окружения из .env
- хранятся настройки приложения
- настраиваются JWT-параметры
- задаются параметры базы данных

Файл НЕ:
- запускает FastAPI
- выполняет SQL-запросы
- содержит бизнес-логику
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек приложения.

    Все значения автоматически читаются
    из переменных окружения или .env файла.
    """

    # Название приложения
    app_name: str = "auth-service"

    # Текущее окружение
    # local / dev / prod / test
    env: str = "local"

    # Секретный ключ для подписи JWT
    jwt_secret: str = "change_me_super_secret"

    # Алгоритм подписи JWT
    jwt_alg: str = "HS256"

    # Время жизни access token в минутах
    access_token_expire_minutes: int = 60

    # Путь к SQLite базе данных
    sqlite_path: str = "./auth.db"

    # Конфигурация pydantic-settings
    model_config = SettingsConfigDict(
        # Файл переменных окружения
        env_file=".env",
        # Кодировка файла
        env_file_encoding="utf-8",
        # Игнорировать лишние поля
        extra="ignore",
    )


# Глобальный объект настроек
# Импортируется во всё приложение
settings = Settings()
