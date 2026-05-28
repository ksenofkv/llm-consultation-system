# bot_service/app/infra/redis.py

"""
Redis-клиент Bot Service.

Здесь:
- создаётся единая точка доступа к Redis
- возвращается redis.asyncio.Redis клиент
- используется settings.redis_url
- клиент создаётся один раз и переиспользуется
- в тестах этот слой мокается через fakeredis

Файл НЕ:
- содержит бизнес-логику
- работает напрямую с LLM
- создаёт Celery задачи
"""

import redis.asyncio as redis

from app.core.config import settings

# Глобальный объект клиента Redis
_redis_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    """
    Возвращает Redis клиент.

    Используется во всех частях Bot Service.
    """

    global _redis_client

    if _redis_client is None:
        _redis_client = redis.Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    return _redis_client
