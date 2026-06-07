from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.core.security import verify_token
from tests.utils.user import register_user
from tests.utils.utils import random_lower_string


async def test_read_user(client: AsyncClient) -> None:
    user_in, access_token = await register_user(client)
    token_data = verify_token(access_token)
    response = await client.get(f"{settings.API_V1_STR}/users/{token_data.user_id}")
    assert response.status_code == status.HTTP_200_OK
    user_out = response.json()
    assert user_out["email"] == user_in["email"]
    assert user_out["username"] == user_in["username"]
    assert user_out["date_of_birth"] == user_in["date_of_birth"]
    assert user_out["is_active"]


async def test_read_user_not_found(client: AsyncClient) -> None:
    response = await client.get(f"{settings.API_V1_STR}/users/{999}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_read_users(client: AsyncClient) -> None:
    await register_user(client)
    await register_user(client)
    response = await client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == status.HTTP_200_OK
    all_users = response.json()
    assert len(all_users) == 2
    for user in all_users:
        assert "email" in user
        assert "username" in user
        assert "date_of_birth" in user
        assert "is_active" in user


async def test_update_user_me(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    new_username = random_lower_string()
    data = {"username": new_username}
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me", json=data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["username"] == new_username


async def test_update_user_me_username_already_taken(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    user_in, _ = await register_user(client)
    data = {"username": user_in["username"]}
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me", json=data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Email or username already taken"


async def test_update_user_me_email_already_taken(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    user_in_2, _ = await register_user(client)
    data = {"email": user_in_2["email"]}
    response = await client.patch(
        f"{settings.API_V1_STR}/users/me", json=data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Email or username already taken"


async def test_delete_user_me(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await client.delete(
        f"{settings.API_V1_STR}/users/me", headers=auth_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    token = auth_headers["Authorization"].removeprefix("Bearer ")
    token_data = verify_token(token)
    response = await client.get(f"{settings.API_V1_STR}/users/{token_data.user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
