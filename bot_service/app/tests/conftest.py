# bot_service/tests/conftest.py

"""
Тестовая инфраструктура Bot Service.

Здесь:
- создаётся fake Redis через fakeredis
- мокается get_redis()
- подготавливаются общие pytest fixtures
- предотвращается подключение к реальному Redis

ВАЖНО:
Патчить нужно именно:
app.bot.handlers.get_redis

Иначе handlers.py продолжит использовать
реальный redis:6379.
"""

# Fake Redis для тестов
import fakeredis.aioredis
import pytest

# Модуль handlers, где используется get_redis
import app.bot.handlers as handlers_module


@pytest.fixture
async def fake_redis():
    """
    Создание fake Redis клиента.

    Используется вместо реального Redis.
    """

    redis_client = fakeredis.aioredis.FakeRedis(
        decode_responses=True,
    )

    yield redis_client

    await redis_client.flushall()
    await redis_client.aclose()


@pytest.fixture(autouse=True)
async def patch_get_redis(
    monkeypatch,
    fake_redis,
):
    """
    Автоматический патч get_redis().

    Все handlers будут использовать fake Redis.
    """

    monkeypatch.setattr(
        handlers_module,
        "get_redis",
        lambda: fake_redis,
    )
