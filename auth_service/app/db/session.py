# auth_service/app/db/session.py

"""
Файл подключения к базе данных Auth Service.

Здесь:
- создаётся асинхронный SQLAlchemy engine
- создаётся фабрика AsyncSession
- формируется строка подключения к БД

Файл НЕ:
- выполняет SQL-запросы
- содержит ORM-модели
- открывает сессии автоматически
"""

# Асинхронный engine SQLAlchemy
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Глобальные настройки приложения
from app.core.config import settings


# Формирование DATABASE_URL для SQLite
DATABASE_URL = f"sqlite+aiosqlite:///{settings.sqlite_path}"


# Создание асинхронного engine
engine = create_async_engine(
    # Строка подключения
    DATABASE_URL,
    # Логирование SQL-запросов
    echo=False,
)


# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    # Engine подключения
    bind=engine,
    # Класс асинхронной сессии
    class_=AsyncSession,
    # Не сбрасывать объекты после commit
    expire_on_commit=False,
)
