"""Async tests for the User API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient) -> None:
    payload = {
        "email": "new@example.com",
        "username": "newuser",
        "password": "securepassword123",
        "full_name": "New User",
    }
    response = await async_client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["username"] == "newuser"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio
async def test_list_users(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_create_user_validation_error(async_client: AsyncClient) -> None:
    payload = {
        "email": "invalid-email",
        "username": "ab",
        "password": "short",
    }
    response = await async_client.post("/api/v1/users", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user_not_found(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
