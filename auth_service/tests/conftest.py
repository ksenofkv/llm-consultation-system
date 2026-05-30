# auth_service/tests/conftest.py

"""
Подготовка тестовой БД.

Перед запуском тестов создаются все таблицы.
После завершения тестов таблицы удаляются.
"""

import pytest_asyncio

from app.db.base import Base
from app.db.session import engine

# обязательно импортируем модели


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
