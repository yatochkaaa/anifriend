from sqlalchemy.ext.asyncio import AsyncSession

from app.models.genre import Genre


async def create_test_genres(session: AsyncSession) -> list[Genre]:
    test_genres = [
        Genre(shikimori_id=1, kind="genre", name="Action", russian="Экшен"),
        Genre(shikimori_id=27, kind="demographic", name="Shounen", russian="Сёнен"),
    ]
    for genre in test_genres:
        session.add(genre)
    await session.flush()
    return test_genres
