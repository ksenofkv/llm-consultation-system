# auth_service/app/core/security.py

"""
Файл безопасности Auth Service.

Здесь:
- хешируются пароли через bcrypt
- проверяются пароли пользователей
- создаются JWT-токены
- декодируются и валидируются JWT-токены

Файл НЕ:
- работает с базой данных
- запускает FastAPI
- содержит бизнес-логику регистрации или логина
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# Настройка bcrypt для хеширования паролей
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Хеширует обычный пароль пользователя.

    На вход получает пароль в виде строки.
    Возвращает безопасный bcrypt-хеш.
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Проверяет обычный пароль против сохранённого хеша.

    Возвращает True, если пароль корректный.
    Возвращает False, если пароль неверный.
    """

    return pwd_context.verify(plain_password, password_hash)


def create_access_token(
    *,
    subject: str | int,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Создаёт JWT access token.

    В payload обязательно добавляются:
    - sub: id пользователя
    - role: роль пользователя
    - iat: время выпуска токена
    - exp: время истечения токена
    """

    now = datetime.now(timezone.utc)

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.access_token_expire_minutes
        )

    expire = now + expires_delta

    payload: dict[str, Any] = {
        "sub": str(subject),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Декодирует и валидирует JWT-токен.

    Проверяет:
    - подпись токена
    - срок действия exp
    - корректность структуры JWT

    Возвращает payload токена.
    """

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )

        return payload

    except ExpiredSignatureError as exc:
        raise ValueError("Token expired") from exc

    except JWTError as exc:
        raise ValueError("Invalid token") from exc