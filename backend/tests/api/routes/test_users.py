from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.core.security import verify_token
from tests.utils.utils import random_email, random_lower_string


async def test_read_user(client: AsyncClient) -> None:
    email = random_email()
    username = random_lower_string()
    data = {
        "email": email,
        "username": username,
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }

    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    access_token = response.json()["access_token"]
    token_data = verify_token(access_token)
    response = await client.get(f"{settings.API_V1_STR}/users/{token_data.user_id}")
    assert response.status_code == status.HTTP_200_OK
    user = response.json()

    assert user["email"] == data["email"]
    assert user["username"] == data["username"]
    assert user["date_of_birth"] == data["date_of_birth"]
    assert user["is_active"]


async def test_read_users(client: AsyncClient) -> None:
    email, email2 = random_email(), random_email()
    username, username2 = random_lower_string(), random_lower_string()
    data = {
        "email": email,
        "username": username,
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    data2 = {
        "email": email2,
        "username": username2,
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    await client.post(f"{settings.API_V1_STR}/auth/register", json=data2)

    response = await client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == status.HTTP_200_OK
    all_users = response.json()
    assert len(all_users) > 1
    for user in all_users:
        assert "email" in user
        assert "username" in user
        assert "date_of_birth" in user
        assert "is_active" in user


async def test_update_user(client: AsyncClient) -> None:
    email = random_email()
    username = random_lower_string()
    new_username = random_lower_string()
    data = {
        "email": email,
        "username": username,
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    access_token = response.json()["access_token"]
    token_data = verify_token(access_token)
    data = {"username": new_username}
    response = await client.patch(
        f"{settings.API_V1_STR}/users/{token_data.user_id}", json=data
    )
    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["username"] == new_username


async def test_delete_user(client: AsyncClient) -> None:
    email = random_email()
    username = random_lower_string()
    data = {
        "email": email,
        "username": username,
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    access_token = response.json()["access_token"]
    token_data = verify_token(access_token)
    response = await client.delete(f"{settings.API_V1_STR}/users/{token_data.user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    response = await client.get(f"{settings.API_V1_STR}/users/{token_data.user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
