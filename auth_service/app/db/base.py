# auth_service/app/db/base.py

"""
Базовый класс SQLAlchemy для Auth Service.

Здесь:
- создаётся единый Base для ORM-моделей
- хранится общая декларативная база SQLAlchemy

Файл НЕ:
- содержит модели пользователей
- выполняет SQL-запросы
- создаёт подключение к БД
"""

# Базовый декларативный класс SQLAlchemy 2.0
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Единая базовая ORM-модель.

    Все модели приложения
    наследуются от этого класса.
    """

    pass