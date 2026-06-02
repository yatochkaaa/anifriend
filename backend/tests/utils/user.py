from httpx import AsyncClient

from app.core.config import settings
from tests.utils.utils import random_email, random_lower_string


async def register_user(client: AsyncClient) -> tuple[dict, str]:
    data = {
        "email": random_email(),
        "username": random_lower_string(),
        "date_of_birth": "1998-08-05",
        "password": "TestPass123",
        "password_repeat": "TestPass123",
    }
    response = await client.post(f"{settings.API_V1_STR}/auth/register", json=data)
    access_token = response.json()["access_token"]
    return data, access_token
