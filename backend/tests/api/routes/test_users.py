from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
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
