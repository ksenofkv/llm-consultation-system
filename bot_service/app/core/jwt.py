# bot_service/app/core/jwt.py

"""
JWT-проверка Bot Service.

Здесь:
- выполняется проверка JWT-токена
- проверяется подпись JWT
- проверяется срок действия exp
- возвращается payload токена

Файл НЕ:
- создаёт JWT
- работает с БД
- обращается к Auth Service
"""

from typing import Any

# JWT библиотека
from jose import (
    ExpiredSignatureError,
    JWTError,
    jwt,
)

# Настройки приложения
from app.core.config import settings


def decode_and_validate(
    token: str,
) -> dict[str, Any]:
    """
    Проверка JWT токена.

    Проверяется:
    - подпись JWT
    - срок действия exp
    - корректность структуры

    Возвращает:
    - payload токена

    Ошибки:
    - ValueError("Token expired")
    - ValueError("Invalid token")
    """

    try:
        # Декодирование и проверка JWT
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )

        # Проверка обязательного поля sub
        if "sub" not in payload:
            raise ValueError("Invalid token")

        return payload

    # JWT истёк
    except ExpiredSignatureError as exc:
        raise ValueError("Token expired") from exc

    # JWT повреждён или подпись неверна
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
