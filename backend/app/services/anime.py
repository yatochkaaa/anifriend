from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Anime, anime_genres


async def get_animes(
    session: AsyncSession,
    *,
    limit: int = 10,
    offset: int = 0,
    score_min: float | None = None,
    genre_ids: list[int] | None = None,
    search: str | None = None,
) -> Sequence[Anime]:
    stmt = select(Anime)

    if score_min is not None:
        stmt = stmt.where(Anime.score >= score_min)
    if genre_ids:
        genres_subq = select(anime_genres.c.anime_id).where(
            anime_genres.c.genre_id.in_(genre_ids)
        )
        stmt = stmt.where(Anime.id.in_(genres_subq))
    if search:
        stmt = stmt.where(Anime.name.ilike(f"%{search}%"))

    stmt = stmt.limit(limit).offset(offset).options(selectinload(Anime.genres))
    result = await session.execute(stmt)
    return result.scalars().all()
