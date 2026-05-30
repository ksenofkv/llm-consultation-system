# auth_service/app/repositories/users.py

"""
Репозиторий пользователей Auth Service.

Здесь:
- выполняются операции с БД
- выполняется поиск пользователей
- создаются пользователи

Файл НЕ:
- проверяет JWT
- создаёт токены
- проверяет пароли
- выбрасывает HTTPException
"""

# SQLAlchemy select
from sqlalchemy import select

# Асинхронная сессия SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession

# ORM модель пользователя
from app.db.models import User


class UsersRepository:
    """
    Репозиторий доступа к таблице users.
    """

    def __init__(self, db: AsyncSession):
        """
        Получает AsyncSession через dependency.
        """

        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Получение пользователя по ID.

        Возвращает:
        - User
        - None
        """

        query = select(User).where(User.id == user_id)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Получение пользователя по email.

        Возвращает:
        - User
        - None
        """

        query = select(User).where(User.email == email)

        result = await self.db.execute(query)

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        email: str,
        password_hash: str,
        role: str = "user",
    ) -> User:
        """
        Создание нового пользователя.
        """

        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
        )

        # Добавление объекта в сессию
        self.db.add(user)

        # Сохранение изменений
        await self.db.commit()

        # Обновление объекта из БД
        await self.db.refresh(user)

        return user
