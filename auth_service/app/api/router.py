# auth_service/app/api/router.py

"""
Главный router Auth Service.

Здесь:
- собираются все router-ы приложения
- подключаются endpoint-модули
- формируется единый API router

Файл НЕ:
- содержит бизнес-логику
- выполняет SQL-запросы
- создаёт FastAPI приложение
"""

# Главный APIRouter FastAPI
from fastapi import APIRouter

# Router auth endpoint-ов
from app.api.routes_auth import router as auth_router


# Общий router приложения
router = APIRouter()


# Подключение auth router
router.include_router(auth_router)