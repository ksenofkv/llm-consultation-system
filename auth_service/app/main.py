#auth_service/app/main.py
"""
Точка входа Auth Service.
Сборка FastAPI-приложения: роутеры, обработчики, lifespan.
Бизнес-логика и SQL вынесены в отдельные модули.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import BaseHTTPException
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Управление жизненным циклом приложения.
    Инициализация БД при старте, закрытие соединений при остановке.
    """
    # === STARTUP ===
    # Создаём таблицы (для SQLite/dev; в prod используйте Alembic миграции)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # Приложение работает
    
    # === SHUTDOWN ===
    # Закрываем соединения с БД
    await engine.dispose()


# === Обработчики исключений ===

async def base_http_exception_handler(request: Request, exc: BaseHTTPException) -> JSONResponse:
    """Обрабатывает кастомные исключения из app.core.exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=getattr(exc, "headers", None),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Обрабатывает ошибки валидации Pydantic (422)."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "body": exc.body,
        },
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """
    Обрабатывает ошибки целостности БД (дубликаты уникальных полей).
    Перехватывает на уровне SQLAlchemy и возвращает понятный клиенту ответ.
    """
    # Простая эвристика для определения дубликата email
    if "users_email" in str(exc.orig) or "UNIQUE constraint failed: users.email" in str(exc.orig):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "User with this email already exists"},
        )
    # Для остальных ошибок БД — 500
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error"},
    )


# === Фабрика приложения ===

def create_app() -> FastAPI:
    """
    Factory-функция для создания экземпляра FastAPI.
    Позволяет легко тестировать приложение и переиспользовать конфигурацию.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Сервис аутентификации и выдачи JWT-токенов",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENV != "production" else None,
        redoc_url="/redoc" if settings.ENV != "production" else None,
        openapi_url="/openapi.json" if settings.ENV != "production" else None,
    )

    # Подключаем API-роутеры
    app.include_router(api_router, prefix="/api")

    # Регистрируем обработчики исключений
    app.add_exception_handler(BaseHTTPException, base_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)

    # === Системные эндпоинты ===

    @app.get("/health", status_code=status.HTTP_200_OK, include_in_schema=False)
    async def health_check() -> dict[str, str]:
        """
        Health check для оркестраторов (K8s, Docker Compose).
        Проверяет подключение к БД.
        """
        try:
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "unhealthy", "database": "disconnected"},
            )

    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        """Корневой эндпоинт с информацией о сервисе."""
        return {
            "service": settings.APP_NAME,
            "environment": settings.ENV,
            "docs": "/docs" if settings.ENV != "production" else None,
        }

    return app


# === Точка входа для uvicorn ===
# Создаём экземпляр приложения для запуска через: uvicorn app.main:app
app = create_app()

