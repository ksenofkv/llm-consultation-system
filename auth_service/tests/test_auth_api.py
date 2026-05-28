# auth_service/tests/test_auth_api.py

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_register_returns_success_status():
    email = f"user_{uuid.uuid4()}@test.com"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "email": email,
            "password": "12345678",
        })

    assert response.status_code in (200, 201)


@pytest.mark.asyncio
async def test_register_response_contains_id():
    email = f"user_{uuid.uuid4()}@test.com"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "email": email,
            "password": "12345678",
        })

    assert "id" in response.json()


@pytest.mark.asyncio
async def test_register_response_contains_email():
    email = f"user_{uuid.uuid4()}@test.com"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "email": email,
            "password": "12345678",
        })

    assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_register_response_contains_role():
    email = f"user_{uuid.uuid4()}@test.com"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "email": email,
            "password": "12345678",
        })

    assert "role" in response.json()


@pytest.mark.asyncio
async def test_register_response_does_not_contain_password_hash():
    email = f"user_{uuid.uuid4()}@test.com"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/register", json={
            "email": email,
            "password": "12345678",
        })

    assert "password_hash" not in response.json()
    assert "password" not in response.json()


@pytest.mark.asyncio
async def test_login_returns_success_status():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})

        response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_response_contains_access_token():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})

        response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })

    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_response_contains_bearer_token_type():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})

        response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })

    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_me_returns_success_with_valid_token():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})
        login_response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })
        token = login_response.json()["access_token"]

        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_me_response_contains_id():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})
        login_response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })
        token = login_response.json()["access_token"]

        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })

    assert "id" in response.json()


@pytest.mark.asyncio
async def test_me_response_contains_email():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})
        login_response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })
        token = login_response.json()["access_token"]

        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })

    assert response.json()["email"] == email


@pytest.mark.asyncio
async def test_me_response_contains_role():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})
        login_response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })
        token = login_response.json()["access_token"]

        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })

    assert "role" in response.json()


@pytest.mark.asyncio
async def test_me_response_contains_created_at():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})
        login_response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })
        token = login_response.json()["access_token"]

        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })

    assert "created_at" in response.json()


@pytest.mark.asyncio
async def test_me_response_does_not_contain_password_hash():
    email = f"user_{uuid.uuid4()}@test.com"
    password = "12345678"

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/auth/register", json={"email": email, "password": password})
        login_response = await client.post("/auth/login", data={
            "username": email,
            "password": password,
        })
        token = login_response.json()["access_token"]

        response = await client.get("/auth/me", headers={
            "Authorization": f"Bearer {token}",
        })

    assert "password_hash" not in response.json()
    assert "password" not in response.json()