# auth_service/tests/test_auth_api.py

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_register_login_me_flow():

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        # Регистрация
        register_response = await client.post(
            "/auth/register",
            json={
                "email": "user@test.com",
                "password": "12345678",
            },
        )

        assert register_response.status_code in (200, 201)

        # Логин
        login_response = await client.post(
            "/auth/login",
            data={
                "username": "user@test.com",
                "password": "12345678",
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        # Получение профиля
        me_response = await client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert me_response.status_code == 200

        user_data = me_response.json()

        assert user_data["email"] == "user@test.com"
        assert "id" in user_data
        assert "role" in user_data