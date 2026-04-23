# auth_service/test_config.py
from app.core.config import settings

print(f"APP_NAME: {settings.APP_NAME}")
print(f"ENV: {settings.ENV}")
print(f"JWT_SECRET задан: {bool(settings.JWT_SECRET)}")
print(f"DB URL: {settings.async_db_url}")
print(f"Is production: {settings.is_production}")