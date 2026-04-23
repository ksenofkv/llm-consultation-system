#auth_service/app/core/config.py
"""
Конфигурация приложения через pydantic-settings.
Читает переменные окружения и формирует единый объект settings.
Только конфигурация — без запуска приложения и без запросов к БД.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки Auth Service.
    
    Все поля читаются из переменных окружения или файла .env.
    """
    
    # === Настройка загрузки конфигурации ===
    model_config = SettingsConfigDict(
        env_file=".env",              # Файл с переменными окружения
        env_file_encoding="utf-8",    # Кодировка файла
        case_sensitive=False,         # Игнорировать регистр имён переменных
        extra="ignore",               # Игнорировать неизвестные переменные
    )

    # === Приложение ===
    APP_NAME: str = Field(default="auth-service", description="Имя сервиса")
    ENV: str = Field(default="local", description="Окружение: local, staging, production")

    # === JWT ===
    JWT_SECRET: str = Field(..., description="Секретный ключ для подписи JWT")
    JWT_ALG: str = Field(default="HS256", description="Алгоритм подписи JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60, 
        description="Время жизни токена доступа в минутах"
    )

    # === База данных ===
    SQLITE_PATH: str = Field(
        default="./auth.db", 
        description="Путь к SQLite-файлу (для разработки)"
    )
    DATABASE_URL: str | None = Field(
        default=None, 
        description="Полная строка подключения к БД (для продакшена)"
    )

    # === Вспомогательные свойства ===
    
    @property
    def async_db_url(self) -> str:
        """
        Возвращает строку подключения для async SQLAlchemy.
        Приоритет: DATABASE_URL > SQLITE_PATH.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"
    
    @property
    def is_production(self) -> bool:
        """Удобный чекер для условной логики в коде."""
        return self.ENV.lower() in ("production", "prod")


# === Глобальный экземпляр настроек ===
# Импортируйте `settings` в других модулях для доступа к конфигурации
settings = Settings()