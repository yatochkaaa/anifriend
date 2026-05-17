from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Genre


async def get_genres(session: AsyncSession) -> Sequence[Genre]:
    genres = await session.execute(select(Genre))
    return genres.scalars().all()
