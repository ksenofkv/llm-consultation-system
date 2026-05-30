# auth_service/app/api/routes_auth.py

"""
Auth endpoint-ы FastAPI.

Здесь:
- описываются HTTP-маршруты Auth Service
- принимаются входные данные
- вызывается usecase-логика
- возвращаются ответы API

Файл НЕ:
- выполняет SQL-запросы
- создаёт JWT напрямую
- содержит бизнес-логику
"""

# FastAPI инструменты
from fastapi import APIRouter, Depends

# OAuth2 form-data логин
from fastapi.security import OAuth2PasswordRequestForm

# Dependencies приложения
from app.api.deps import (
    get_auth_uc,
    get_current_user,
)

# UseCase авторизации
from app.usecases.auth import AuthUseCase

# Pydantic схемы
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
)

from app.schemas.user import UserPublic


# Router Auth Service
router = APIRouter(
    # Все endpoint-ы начинаются с /auth
    prefix="/auth",
    # Swagger tag
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=201,
)
async def register(
    data: RegisterRequest,
    auth_uc: AuthUseCase = Depends(get_auth_uc),
):
    """
    Регистрация нового пользователя.

    Endpoint:
    POST /auth/register
    """

    user = await auth_uc.register(
        email=data.email,
        password=data.password,
    )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
):
    """
    Логин пользователя.

    Endpoint:
    POST /auth/login

    OAuth2PasswordRequestForm автоматически
    принимает form-data:
    - username
    - password

    username используется как email.
    """

    access_token = await auth_uc.login(
        email=form.username,
        password=form.password,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserPublic,
)
async def me(
    current_user: UserPublic = Depends(get_current_user),
):
    """
    Получение текущего пользователя.

    Endpoint:
    GET /auth/me

    Требует:
    Authorization: Bearer <jwt>
    """

    return current_user
