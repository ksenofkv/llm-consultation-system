from fastapi import APIRouter

# Создаём общий роутер, к которому будем подключать модульные
api_router = APIRouter()

# Пока ничего не подключаем — файл создан, чтобы убрать ошибку импорта
# Позже добавим:
# from app.api.routes_auth import router as auth_router
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
