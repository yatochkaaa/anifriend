import asyncio
from typing import TypedDict

import httpx
from sqlalchemy import insert

from app.core.db import async_session_maker
from app.integrations.shikimori import ShikimoriClient
from app.models.genre import Genre


class GenreValues(TypedDict):
    shikimori_id: int
    kind: str
    name: str
    russian: str


async def seed_genres() -> None:
    async with httpx.AsyncClient() as client:
        shikimori_client = ShikimoriClient(client)
        shikimori_genres = await shikimori_client.get_genres()

    async with async_session_maker() as session:
        db_genres: list[GenreValues] = [
            {
                "shikimori_id": genre.id,
                "kind": genre.kind,
                "name": genre.name,
                "russian": genre.russian,
            }
            for genre in shikimori_genres
        ]
        await session.execute(insert(Genre).values(db_genres))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(
        seed_genres(),
        loop_factory=asyncio.SelectorEventLoop,
    )
