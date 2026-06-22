from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dto import SurveyCreateDTO, SurveyUpdateDTO
from app.exceptions import SurveyAlreadyExistsError
from app.models import Anime, Survey, SurveyGenre


async def get_survey(session: AsyncSession, user_id: int) -> Survey | None:
    survey_result = await session.execute(
        select(Survey)
        .where(Survey.user_id == user_id)
        .options(
            selectinload(Survey.genres),
            selectinload(Survey.animes),
        )
    )
    db_survey = survey_result.scalar_one_or_none()

    if db_survey is None:
        return None

    return db_survey


async def add_survey(session: AsyncSession, dto: SurveyCreateDTO) -> Survey:
    animes_result = await session.execute(
        select(Anime).where(Anime.id.in_(dto["animes"]))
    )
    db_animes = list(animes_result.scalars())
    survey = Survey(
        user_id=dto["user_id"],
        genres=[
            SurveyGenre(genre_id=genre["genre_id"], is_liked=genre["is_liked"])
            for genre in dto["genres"]
        ],
        animes=db_animes,
    )

    session.add(survey)

    try:
        await session.flush()
    except IntegrityError:
        raise SurveyAlreadyExistsError

    return survey


async def modify_survey(session: AsyncSession, dto: SurveyUpdateDTO) -> Survey | None:
    animes_result = await session.execute(
        select(Anime).where(Anime.id.in_(dto["animes"]))
    )
    db_animes = list(animes_result.scalars())

    survey_result = await session.execute(
        select(Survey)
        .where(Survey.user_id == dto["user_id"])
        .options(
            selectinload(Survey.genres),
            selectinload(Survey.animes),
        )
    )
    db_survey = survey_result.scalar_one_or_none()

    if db_survey is None:
        return None

    db_survey.genres = [
        SurveyGenre(genre_id=genre["genre_id"], is_liked=genre["is_liked"])
        for genre in dto["genres"]
    ]
    db_survey.animes = db_animes

    await session.flush()

    return db_survey
