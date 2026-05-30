# bot_service/app/main.py

"""
FastAPI-приложение Bot Service.

Здесь:
- создаётся FastAPI для Bot Service (например для /health)
- подключаются служебные маршруты
- можно запускать aiogram через отдельный entrypoint
- файл НЕ содержит логику общения с LLM
- файл НЕ работает напрямую с Redis
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI


# Общие маршруты (например /health)
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle FastAPI для запуска и остановки приложения.
    """
    # Здесь можно запускать подготовительные задачи
    # Например, проверка подключения к брокеру или Redis
    yield
    # Здесь можно корректно завершать процессы
    # Например, закрытие подключений


# Создание FastAPI приложения
app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)


@app.get("/health")
async def healthcheck():
    """
    Проверка состояния сервиса.
    """

    return {
        "status": "ok",
    }
