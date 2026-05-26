# auth_service/app/db/models.py

"""
ORM-модели Auth Service.

Здесь:
- описываются таблицы базы данных
- создаются SQLAlchemy ORM-модели
- задаются поля и ограничения таблиц

Файл НЕ:
- содержит бизнес-логику
- выполняет регистрацию или логин
- создаёт JWT
"""

from datetime import datetime

# SQLAlchemy типы данных
from sqlalchemy import DateTime, Integer, String, func

# ORM mapping
from sqlalchemy.orm import Mapped, mapped_column

# Базовый класс всех ORM-моделей
from app.db.base import Base


class User(Base):
    """
    ORM-модель пользователя.

    Таблица хранит:
    - email пользователя
    - bcrypt hash пароля
    - роль пользователя
    - дату создания
    """

    # Название таблицы в БД
    __tablename__ = "users"

    # ID пользователя
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Email пользователя
    # unique=True создаёт уникальный индекс
    # и защищает БД от дублей
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    # bcrypt hash пароля
    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Роль пользователя
    # Например: user / admin
    role: Mapped[str] = mapped_column(
        String,
        default="user",
        nullable=False,
    )

    # Дата создания пользователя
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),

        # Время выставляется автоматически
        server_default=func.now(),

        nullable=False,
    )