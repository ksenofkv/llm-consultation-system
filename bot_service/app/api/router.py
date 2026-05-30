# bot_service/app/api/router.py

"""
Сборка роутеров Bot Service.

Здесь подключаются все API-роутеры FastAPI.
Файл нужен для централизованной регистрации маршрутов.
"""

from fastapi import APIRouter

router = APIRouter()
