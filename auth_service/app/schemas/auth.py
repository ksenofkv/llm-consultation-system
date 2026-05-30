# auth_service/app/schemas/auth.py

"""
Pydantic-схемы Auth Service.

Здесь:
- описываются схемы регистрации
- описываются схемы JWT-токенов
- валидируются входные данные API

Файл НЕ:
- работает с БД
- создаёт JWT
- содержит бизнес-логику
"""

# EmailStr валидирует email автоматически
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """
    Схема регистрации пользователя.

    Используется в:
    POST /auth/register
    """

    # Email пользователя
    email: EmailStr

    # Пароль пользователя
    password: str


class TokenResponse(BaseModel):
    """
    Схема ответа с JWT-токеном.

    Используется после логина.
    """

    # JWT access token
    access_token: str

    # Тип токена
    # Обычно Bearer
    token_type: str = "bearer"


class LoginResponse(TokenResponse):
    """
    Отдельная схема логина.

    Наследуется от TokenResponse.
    Можно расширять дополнительными полями.
    """

    pass
