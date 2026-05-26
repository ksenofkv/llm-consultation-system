# auth_service/app/usecases/auth.py

"""
Usecase-слой Auth Service.

Здесь:
- реализуется бизнес-логика регистрации
- реализуется бизнес-логика логина
- реализуется получение текущего пользователя
- используются репозитории, security-функции и кастомные исключения

Файл НЕ:
- выполняет SQL-запросы напрямую
- содержит FastAPI endpoint-ы
- работает с HTTP-зависимостями
"""

# Функции безопасности:
# - хеширование пароля
# - проверка пароля
# - создание JWT
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

# Кастомные исключения приложения
from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

# Репозиторий пользователей
from app.repositories.users import UsersRepository

# Схема публичного пользователя
from app.schemas.user import UserPublic


class AuthUseCase:
    """
    Бизнес-логика Auth Service.

    Этот класс не знает, как устроен FastAPI endpoint.
    Он работает только с репозиторием и функциями безопасности.
    """

    def __init__(self, users_repo: UsersRepository):
        """
        Получает репозиторий пользователей через dependency.
        """

        self.users_repo = users_repo

    async def register(
        self,
        *,
        email: str,
        password: str,
    ) -> UserPublic:
        """
        Регистрация нового пользователя.

        Шаги:
        1. Проверяем, существует ли пользователь с таким email.
        2. Если существует — выбрасываем UserAlreadyExistsError.
        3. Хешируем пароль.
        4. Создаём пользователя через репозиторий.
        5. Возвращаем публичную схему пользователя.
        """

        existing_user = await self.users_repo.get_by_email(email)

        if existing_user is not None:
            raise UserAlreadyExistsError()

        password_hash = hash_password(password)

        user = await self.users_repo.create(
            email=email,
            password_hash=password_hash,
            role="user",
        )

        return UserPublic.model_validate(user)

    async def login(
        self,
        *,
        email: str,
        password: str,
    ) -> str:
        """
        Логин пользователя.

        Шаги:
        1. Ищем пользователя по email.
        2. Если пользователь не найден — InvalidCredentialsError.
        3. Проверяем пароль.
        4. Если пароль неверный — InvalidCredentialsError.
        5. Создаём JWT access token.
        6. Возвращаем токен.
        """

        user = await self.users_repo.get_by_email(email)

        if user is None:
            raise InvalidCredentialsError()

        is_password_valid = verify_password(
            plain_password=password,
            password_hash=user.password_hash,
        )

        if not is_password_valid:
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=user.id,
            role=user.role,
        )

        return access_token

    async def me(
        self,
        *,
        user_id: int,
    ) -> UserPublic:
        """
        Получение текущего пользователя по user_id из JWT.

        Шаги:
        1. Получаем user_id из dependency.
        2. Ищем пользователя в БД через репозиторий.
        3. Если пользователь не найден — UserNotFoundError.
        4. Возвращаем публичную схему пользователя.
        """

        user = await self.users_repo.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return UserPublic.model_validate(user)