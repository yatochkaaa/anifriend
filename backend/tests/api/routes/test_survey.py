from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.models.genre import Genre


async def test_create_survey(
    client: AsyncClient, auth_headers: dict[str, str], genres: list[Genre]
) -> None:
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    response = await client.post(
        f"{settings.API_V1_STR}/survey/", json=data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    survey = response.json()
    assert survey["id"]
    for genre_prefer in genre_prefer_ids:
        assert genre_prefer in survey["genres_prefer"]
    assert survey["genres_avoid"] == []
    assert survey["animes_prefer"] == []
    assert survey["characters_prefer"] == []


async def test_create_survey_duplicate(
    client: AsyncClient, auth_headers: dict[str, str], genres: list[Genre]
) -> None:
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    await client.post(f"{settings.API_V1_STR}/survey/", json=data, headers=auth_headers)
    response = await client.post(
        f"{settings.API_V1_STR}/survey/", json=data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "Survey already exists"


async def test_read_survey(
    client: AsyncClient, auth_headers: dict[str, str], genres: list[Genre]
) -> None:
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    await client.post(f"{settings.API_V1_STR}/survey/", json=data, headers=auth_headers)
    response = await client.get(f"{settings.API_V1_STR}/survey/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    survey = response.json()

    for genre_prefer in genre_prefer_ids:
        assert genre_prefer in survey["genres_prefer"]
    assert survey["genres_avoid"] == []
    assert survey["animes_prefer"] == []
    assert survey["characters_prefer"] == []


async def test_read_survey_not_found(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    response = await client.get(f"{settings.API_V1_STR}/survey/", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_update_survey(
    client: AsyncClient, auth_headers: dict[str, str], genres: list[Genre]
) -> None:
    genre_prefer_ids = [genre.id for genre in genres]
    data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    await client.post(f"{settings.API_V1_STR}/survey/", json=data, headers=auth_headers)

    genre_avoid_ids = [genre_prefer_ids[-1]]
    genre_prefer_ids = genre_prefer_ids[:-1]
    update_data = {
        "genres_prefer": genre_prefer_ids,
        "genres_avoid": genre_avoid_ids,
        "animes_prefer": [],
        "characters_prefer": [],
    }
    response = await client.put(
        f"{settings.API_V1_STR}/survey/", json=update_data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    survey = response.json()
    for genre_prefer in genre_prefer_ids:
        assert genre_prefer in survey["genres_prefer"]
    for genre_avoid in genre_avoid_ids:
        assert genre_avoid in survey["genres_avoid"]
    assert survey["animes_prefer"] == []
    assert survey["characters_prefer"] == []


async def test_update_survey_not_found(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    data = {
        "genres_prefer": [],
        "genres_avoid": [],
        "animes_prefer": [],
        "characters_prefer": [],
    }
    response = await client.put(
        f"{settings.API_V1_STR}/survey/", json=data, headers=auth_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
