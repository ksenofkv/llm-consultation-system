# auth_service/app/core/exceptions.py

"""
Файл HTTP-исключений Auth Service.

Здесь:
- создаются кастомные HTTP-ошибки
- описываются типовые ошибки авторизации
- централизуется обработка ошибок приложения

Файл НЕ:
- работает с БД
- содержит бизнес-логику
- создаёт JWT
"""

# Базовое HTTP-исключение FastAPI
from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    """
    Базовый класс для всех HTTP-ошибок приложения.

    Позволяет создавать собственные исключения
    в едином стиле.
    """

    def __init__(
        self,
        status_code: int,
        detail: str,
    ):

        super().__init__(
            status_code=status_code,
            detail=detail,
        )


class UserAlreadyExistsError(BaseHTTPException):
    """
    Пользователь уже существует.
    HTTP 409 Conflict
    """

    def __init__(self):

        super().__init__(
            status_code=409,
            detail="User already exists",
        )


class InvalidCredentialsError(BaseHTTPException):
    """
    Неверный email или пароль.
    HTTP 401 Unauthorized
    """

    def __init__(self):

        super().__init__(
            status_code=401,
            detail="Invalid credentials",
        )


class InvalidTokenError(BaseHTTPException):
    """
    JWT токен повреждён или неверен.
    HTTP 401 Unauthorized
    """

    def __init__(self):

        super().__init__(
            status_code=401,
            detail="Invalid token",
        )


class TokenExpiredError(BaseHTTPException):
    """
    JWT токен истёк.
    HTTP 401 Unauthorized
    """

    def __init__(self):

        super().__init__(
            status_code=401,
            detail="Token expired",
        )


class UserNotFoundError(BaseHTTPException):
    """
    Пользователь не найден.
    HTTP 404 Not Found
    """

    def __init__(self):

        super().__init__(
            status_code=404,
            detail="User not found",
        )


class PermissionDeniedError(BaseHTTPException):
    """
    Недостаточно прав доступа.
    HTTP 403 Forbidden
    """

    def __init__(self):

        super().__init__(
            status_code=403,
            detail="Permission denied",
        )
