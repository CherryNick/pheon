import pytest
from httpx import AsyncClient
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

LOGIN_URL = "/auth/login"
REFRESH_URL = "/auth/refresh"
LOGOUT_URL = "/auth/logout"

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, user_factory):
    password = "strongpassword123"
    user = user_factory(password_hash=pwd_context.hash(password))
    response = await client.post(LOGIN_URL, json={"username": user.username, "password": password})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, user_factory):
    user = user_factory(password_hash=pwd_context.hash("correctpassword"))

    response = await client.post(LOGIN_URL, json={"username": user.username, "password": "wrongpassword"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_refresh_success(client: AsyncClient, user_factory):
    password = "testpassword"
    user = user_factory(password_hash=pwd_context.hash(password))

    login_resp = await client.post(LOGIN_URL, json={"username": user.username, "password": password})
    refresh_token = login_resp.json()["refresh_token"]

    refresh_resp = await client.post(REFRESH_URL, json={"refresh_token": refresh_token})

    assert refresh_resp.status_code == 200
    data = refresh_resp.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_refresh_invalid_token(client: AsyncClient):
    refresh_resp = await client.post(REFRESH_URL, json={"refresh_token": "invalidtoken"})

    assert refresh_resp.status_code == 401

@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient, user_factory):
    password = "testpassword"
    user = user_factory(password_hash=pwd_context.hash(password))

    login_resp = await client.post(LOGIN_URL, json={"username": user.username, "password": password})
    assert login_resp.status_code == 200

    access_token = login_resp.json()["access_token"]

    logout_resp = await client.post(LOGOUT_URL, headers={"Authorization": f"Bearer {access_token}"})

    assert logout_resp.status_code == 200
