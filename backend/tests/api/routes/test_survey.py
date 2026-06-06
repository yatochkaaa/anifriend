from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.core.security import verify_token
from app.models.genre import Genre
from tests.utils.user import register_user


async def test_create_survey(client: AsyncClient, genres: list[Genre]) -> None:
    _, access_token = await register_user(client)
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post(
        f"{settings.API_V1_STR}/survey/", json=data, headers=headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    survey = response.json()
    assert survey["id"]
    token_data = verify_token(access_token)
    assert token_data.user_id == survey["user_id"]
    for genre_prefer in genre_prefer_ids:
        assert genre_prefer in survey["genres_prefer"]
    assert survey["genres_avoid"] == []
    assert survey["animes_prefer"] == []
    assert survey["characters_prefer"] == []


async def test_create_survey_duplicate(client: AsyncClient, genres: list[Genre]) -> None:
    _, access_token = await register_user(client)
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    await client.post(f"{settings.API_V1_STR}/survey/", json=data, headers=headers)
    response = await client.post(
        f"{settings.API_V1_STR}/survey/", json=data, headers=headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Survey already exists"


async def test_read_survey(client: AsyncClient, genres: list[Genre]) -> None:
    _, access_token = await register_user(client)
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    await client.post(f"{settings.API_V1_STR}/survey/", json=data, headers=headers)
    response = await client.get(f"{settings.API_V1_STR}/survey/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    survey = response.json()

    for genre_prefer in genre_prefer_ids:
        assert genre_prefer in survey["genres_prefer"]
    assert survey["genres_avoid"] == []
    assert survey["animes_prefer"] == []
    assert survey["characters_prefer"] == []


async def test_read_survey_not_found(client: AsyncClient) -> None:
    _, access_token = await register_user(client)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.get(f"{settings.API_V1_STR}/survey/", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_survey(client: AsyncClient, genres: list[Genre]) -> None:
    _, access_token = await register_user(client)
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    await client.post(f"{settings.API_V1_STR}/survey/", json=data, headers=headers)

    genre_avoid_ids = [genre_prefer_ids[-1]]
    genre_prefer_ids = genre_prefer_ids[:-1]
    update_data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": genre_avoid_ids,
        "animes_prefer": [],
        "characters_prefer": [],
    }
    response = await client.put(
        f"{settings.API_V1_STR}/survey/", json=update_data, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    survey = response.json()
    for genre_prefer in genre_prefer_ids:
        assert genre_prefer in survey["genres_prefer"]
    for genre_avoid in genre_avoid_ids:
        assert genre_avoid in survey["genres_avoid"]
    assert survey["animes_prefer"] == []
    assert survey["characters_prefer"] == []
