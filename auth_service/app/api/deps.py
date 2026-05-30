# auth_service/app/api/deps.py

"""
Dependencies Auth Service.

Здесь:
- создаются FastAPI dependencies
- выдаётся AsyncSession
- создаются репозитории
- создаются usecase-объекты
- валидируется JWT
- определяется текущий пользователь

Файл НЕ:
- содержит endpoint-ы
- выполняет SQL напрямую
- содержит бизнес-логику
"""

from collections.abc import AsyncGenerator

# FastAPI dependencies
from fastapi import Depends

# OAuth2 Bearer token
from fastapi.security import OAuth2PasswordBearer

# AsyncSession SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

# JWT decode
from jose import ExpiredSignatureError, JWTError

# Engine session factory
from app.db.session import AsyncSessionLocal

# Репозиторий пользователей
from app.repositories.users import UsersRepository

# UseCase авторизации
from app.usecases.auth import AuthUseCase

# Security decode
from app.core.security import decode_token

# Исключения приложения
from app.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
    UserNotFoundError,
)

# Pydantic схема пользователя
from app.schemas.user import UserPublic


# OAuth2 схема получения Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency выдачи AsyncSession.

    Создаёт сессию на запрос
    и автоматически закрывает её.
    """

    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(
    db: AsyncSession = Depends(get_db),
) -> UsersRepository:
    """
    Dependency репозитория пользователей.
    """

    return UsersRepository(db)


def get_auth_uc(
    users_repo: UsersRepository = Depends(get_users_repo),
) -> AuthUseCase:
    """
    Dependency AuthUseCase.
    """

    return AuthUseCase(users_repo)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    """
    Получение user_id из JWT.

    Проверяется:
    - подпись JWT
    - срок действия exp
    - наличие поля sub
    """

    try:
        payload = decode_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise InvalidTokenError()

        return int(user_id)

    except ExpiredSignatureError as exc:
        raise TokenExpiredError() from exc

    except JWTError as exc:
        raise InvalidTokenError() from exc

    except ValueError as exc:
        error_text = str(exc).lower()

        if "expired" in error_text:
            raise TokenExpiredError() from exc

        raise InvalidTokenError() from exc


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
) -> UserPublic:
    """
    Получение текущего пользователя.

    Используется в:
    - /auth/me
    """

    user = await auth_uc.me(user_id=user_id)

    if user is None:
        raise UserNotFoundError()

    return user
