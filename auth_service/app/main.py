#auth_service/app/main.py

# Импорт contextmanager для корректного lifecycle FastAPI
from contextlib import asynccontextmanager

# Основной класс FastAPI
from fastapi import FastAPI

# Главный router приложения
from app.api.router import router

# Глобальные настройки приложения
from app.core.config import settings

# Базовый класс SQLAlchemy моделей
from app.db.base import Base

# Асинхронный engine SQLAlchemy
from app.db.session import engine


# Lifespan используется вместо deprecated on_event("startup")
# Выполняется при запуске и остановке приложения
@asynccontextmanager
async def lifespan(app: FastAPI):

    # При старте приложения создаём таблицы в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Приложение работает
    yield

    # При остановке приложения закрываем engine
    await engine.dispose()


# Создание экземпляра FastAPI
app = FastAPI(

    # Название приложения из .env / config
    title=settings.app_name,

    # Подключение lifecycle hooks
    lifespan=lifespan,
)


# Подключение всех роутеров приложения
app.include_router(router)


# Системный endpoint проверки состояния сервиса
@app.get("/health")
async def health_check():

    # Возвращаем статус сервиса
    return {
        "status": "ok",
        "service": settings.app_name,
    }