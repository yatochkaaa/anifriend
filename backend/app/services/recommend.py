import asyncio
from itertools import chain

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.shikimori import ShikimoriAnime, ShikimoriClient
from app.services.survey import get_survey

DEFAULT_MIN_SCORE = 7
DEFAULT_RECOMMENDATIONS_LIMIT = 20


def _has_avoided_genre(anime: ShikimoriAnime, genres_avoid: set[int]) -> bool:
    return any(genre.id in genres_avoid for genre in anime.genres)


async def get_recommendations(
    session: AsyncSession,
    shikimori_client: ShikimoriClient,
    score: int = DEFAULT_MIN_SCORE,
) -> list[ShikimoriAnime]:
    survey = await get_survey(session)

    if survey is None:
        return []

    anime_by_genre_requests = [
        shikimori_client.get_anime_by_genre(genre_id, score)
        for genre_id in survey["genres_prefer"]
    ]
    results = await asyncio.gather(*anime_by_genre_requests)

    anime_by_id = {anime.id: anime for anime in chain.from_iterable(results)}
    genres_avoid = set(survey["genres_avoid"])
    filtered_anime = [
        anime
        for anime in anime_by_id.values()
        if not _has_avoided_genre(anime, genres_avoid)
    ]
    filtered_anime.sort(key=lambda anime: anime.score or 0.0, reverse=True)

    return filtered_anime[:DEFAULT_RECOMMENDATIONS_LIMIT]
