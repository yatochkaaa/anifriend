from httpx import AsyncClient
from pydantic import BaseModel

from app.core.config import settings


class ShikimoriGenre(BaseModel):
    id: int
    kind: str
    name: str
    russian: str


class ShikimoriClient:
    URL = settings.SHIKIMORI_URL

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get_genres(self) -> list[ShikimoriGenre]:
        payload = {"query": "{ genres(entryType: Anime) { id kind name russian } }"}
        response = await self._client.post(self.URL, json=payload)
        genres = response.json()["data"]["genres"]
        return [ShikimoriGenre.model_validate(genre) for genre in genres]
