from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.anime import Anime

from .anime import get_animes
from .survey import get_survey

DEFAULT_MIN_SCORE = 7
DEFAULT_RECOMMENDATIONS_LIMIT = 20


async def get_recommendations(
    session: AsyncSession,
    *,
    user_id: int,
) -> Sequence[Anime]:
    survey = await get_survey(session, user_id)

    if survey is None:
        return []

    genre_ids = [sg.genre_id for sg in survey.genres if sg.is_liked]
    animes = await get_animes(
        session,
        limit=DEFAULT_RECOMMENDATIONS_LIMIT,
        score_min=DEFAULT_MIN_SCORE,
        genre_ids=genre_ids,
    )

    return animes
