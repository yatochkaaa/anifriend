import asyncio
from datetime import date, time

from fastapi import status
from httpx import AsyncClient, Response
from pydantic import BaseModel, field_validator

from app.core.config import settings
from app.exceptions import MalRateLimitError


class MalPicture(BaseModel):
    large: str | None = None
    medium: str


class MalAltTitles(BaseModel):
    synonyms: list[str] = []
    en: str | None = None
    ja: str | None = None

    @field_validator("synonyms", mode="before")
    @classmethod
    def _none_to_list(cls, v) -> list[str]:
        return v or []


class MalGenre(BaseModel):
    id: int
    name: str


class MalStartSeason(BaseModel):
    year: int
    season: str


class MalBroadcast(BaseModel):
    day_of_the_week: str
    start_time: time | None = None


class MalStudio(BaseModel):
    id: int
    name: str


class MalAnime(BaseModel):
    id: int
    title: str
    main_picture: MalPicture | None = None
    alternative_titles: MalAltTitles | None = None
    start_date: date | None = None
    end_date: date | None = None
    synopsis: str | None = None
    mean: float | None = None
    rank: int | None = None
    popularity: int | None = None
    nsfw: str | None = None
    genres: list[MalGenre] = []
    media_type: str
    status: str
    num_episodes: int = 0
    start_season: MalStartSeason | None = None
    broadcast: MalBroadcast | None = None
    source: str | None = None
    average_episode_duration: int | None = None
    rating: str | None = None
    studios: list[MalStudio] = []


class MalClient:
    URL = settings.MAL_API_URL
    FIELDS = (
        "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,"
        "rank,popularity,nsfw,genres,media_type,status,num_episodes,start_season,"
        "broadcast,source,average_episode_duration,rating,studios"
    )
    MAX_RETRIES = 5
    THROTTLE = 0.6
    BACKOFF_BASE = 1.0

    def __init__(self, client: AsyncClient, *, client_id: str | None = None) -> None:
        client.headers["X-MAL-CLIENT-ID"] = client_id or settings.MAL_CLIENT_ID
        self._client = client

    async def _get(self, path: str, params: dict) -> Response:
        for attempt in range(self.MAX_RETRIES):
            response = await self._client.get(f"{self.URL}{path}", params=params)
            if (
                response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
                or response.status_code >= 500
            ):
                retry_after = response.headers.get("Retry-After")
                wait = (
                    float(retry_after)
                    if retry_after
                    else self.BACKOFF_BASE * 2**attempt
                )
                await asyncio.sleep(wait)
                continue
            response.raise_for_status()
            await asyncio.sleep(self.THROTTLE)
            return response
        raise MalRateLimitError

    async def list_ranking(
        self, ranking_type: str = "all", limit: int = 500, offset: int = 0
    ) -> list[MalAnime]:
        params = {
            "ranking_type": ranking_type,
            "limit": limit,
            "offset": offset,
            "fields": self.FIELDS,
            "nsfw": "true",
        }
        response = await self._get("/anime/ranking", params)
        data = response.json()

        return [MalAnime.model_validate(item["node"]) for item in data["data"]]
