from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from tests.utils.user import register_user
from tests.utils.utils import random_email, random_lower_string


async def test_register_user(client: AsyncClient) -> None:
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
    assert response.status_code == status.HTTP_201_CREATED
    token = response.json()
    assert token["access_token"]
    assert token["token_type"] == "bearer"


async def test_register_username_already_taken(client: AsyncClient) -> None:
    user_in, _ = await register_user(client)
    email = random_email()
    data = {
        "email": email,
        "username": user_in["username"],
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Email or username already taken"


async def test_register_email_already_taken(client: AsyncClient) -> None:
    user_in, _ = await register_user(client)
    username = random_lower_string()
    data = {
        "email": user_in["email"],
        "username": username,
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Email or username already taken"


async def test_login_username(client: AsyncClient) -> None:
    user_in, _ = await register_user(client)
    login_data = {"username": user_in["username"], "password": user_in["password"]}
    response = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert token["access_token"]
    assert token["token_type"] == "bearer"


async def test_login_email(client: AsyncClient) -> None:
    user_in, _ = await register_user(client)
    login_data = {"username": user_in["email"], "password": user_in["password"]}
    response = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert token["access_token"]
    assert token["token_type"] == "bearer"


async def test_login_incorrect_password(client: AsyncClient) -> None:
    user_in, _ = await register_user(client)
    login_data = {"username": user_in["username"], "password": "WrongPass123"}
    response = await client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect credentials"
