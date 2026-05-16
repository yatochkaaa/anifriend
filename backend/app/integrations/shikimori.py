from httpx import AsyncClient
from pydantic import BaseModel

from app.core.config import settings


class ShikimoriGenre(BaseModel):
    id: int
    kind: str
    name: str
    russian: str


class ShikimoriPoster(BaseModel):
    main_url: str | None = None


class ShikimoriAnime(BaseModel):
    id: int
    name: str
    russian: str | None = None
    score: float | None = None
    kind: str | None = None
    episodes: int = 0
    status: str | None = None
    genres: list[ShikimoriGenre] = []
    poster: ShikimoriPoster | None = None


class ShikimoriClient:
    URL = settings.SHIKIMORI_URL

    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    async def get_genres(self) -> list[ShikimoriGenre]:
        payload = {"query": "{ genres(entryType: Anime) { id kind name russian } }"}
        response = await self._client.post(self.URL, json=payload)
        genres = response.json()["data"]["genres"]
        return [ShikimoriGenre.model_validate(genre) for genre in genres]

    async def get_anime_by_genre(
        self, genre_id: int, score: int, limit: int = 10
    ) -> list[ShikimoriAnime]:
        payload = {
            "query": """
                query($genre: String, $limit: PositiveInt, $score: Int) {
                    animes(genre: $genre, limit: $limit, score: $score) {
                        id name russian score
                        genres { id kind name russian }
                    }
                }
            """,
            "variables": {
                "genre": str(genre_id),
                "limit": limit,
                "score": score,
            },
        }
        response = await self._client.post(self.URL, json=payload)
        animes = response.json()["data"]["animes"]
        return [ShikimoriAnime.model_validate(anime) for anime in animes]
