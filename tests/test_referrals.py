import pytest
from datetime import datetime, timedelta, timezone


@pytest.mark.asyncio
async def test_register_user(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "securepassword"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_create_and_get_referral_code(client):
    # 1. Регистрируемся и логинимся
    await client.post("/api/v1/auth/register", json={"email": "owner@test.com", "password": "pass"})
    login_res = await client.post("/api/v1/auth/login", data={"username": "owner@test.com", "password": "pass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Создаем код
    expires = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    create_res = await client.post(
        "/api/v1/referrals/code",
        json={"code": "PROMO2024", "expires_at": expires},
        headers=headers
    )
    assert create_res.status_code == 200
    assert create_res.json()["code"] == "PROMO2024"

    # 3. Проверяем получение кода по email (публичный эндпоинт)
    get_res = await client.get("/api/v1/referrals/code-by-email?email=owner@test.com")
    assert get_res.status_code == 200
    assert get_res.json() == "PROMO2024"


@pytest.mark.asyncio
async def test_registration_by_referral_code(client):
    # Создаем реферера и его код
    await client.post("/api/v1/auth/register", json={"email": "ref@test.com", "password": "pass"})
    login = await client.post("/api/v1/auth/login", data={"username": "ref@test.com", "password": "pass"})
    token = login.json()["access_token"]

    expires = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    await client.post(
        "/api/v1/referrals/code",
        json={"code": "INVITE_ME", "expires_at": expires},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Регистрируем нового пользователя по коду
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "newbie@test.com", "password": "pass", "referral_code": "INVITE_ME"}
    )
    assert response.status_code == 201
    assert response.json()["referrer_id"] is not None
