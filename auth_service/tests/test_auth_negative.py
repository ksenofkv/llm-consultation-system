# auth_service/tests/test_auth_negative.py

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_duplicate_registration():
    email = f"dup_{uuid.uuid4()}@test.com"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        await client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "12345678",
            },
        )

        response = await client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "12345678",
            },
        )

        assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password():
    email = f"wrong_{uuid.uuid4()}@test.com"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        await client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "12345678",
            },
        )

        response = await client.post(
            "/auth/login",
            data={
                "username": email,
                "password": "wrongpass",
            },
        )

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get("/auth/me")

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:

        response = await client.get(
            "/auth/me",
            headers={
                "Authorization": "Bearer invalid_token",
            },
        )

        assert response.status_code == 401