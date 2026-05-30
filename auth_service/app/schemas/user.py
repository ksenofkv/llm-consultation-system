# auth_service/app/schemas/user.py

"""
Pydantic-схемы пользователя Auth Service.

Здесь:
- описывается публичная модель пользователя
- формируются безопасные ответы API
- скрываются чувствительные данные

Файл НЕ:
- работает с БД
- содержит ORM-модели
- содержит password_hash
"""

from datetime import datetime

# Базовая схема Pydantic
from pydantic import BaseModel, EmailStr

# Настройки совместимости с ORM
from pydantic import ConfigDict


class UserPublic(BaseModel):
    """
    Публичное представление пользователя.

    Используется:
    - в ответах API
    - в /auth/me
    - после регистрации

    ВАЖНО:
    password_hash здесь отсутствует.
    """

    # ID пользователя
    id: int

    # Email пользователя
    email: EmailStr

    # Роль пользователя
    role: str

    # Дата создания пользователя
    created_at: datetime

    # Разрешает создание схемы из ORM объекта
    model_config = ConfigDict(from_attributes=True)
