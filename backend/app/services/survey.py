from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dto import SurveyCreateDTO, SurveyReadDTO, SurveyUpdateDTO
from app.exceptions import SurveyAlreadyExistsError
from app.models import Survey, SurveyAnime, SurveyCharacter, SurveyGenre


def gather_survey_genres(
    prefer_ids: list[int], avoid_ids: list[int]
) -> list[SurveyGenre]:
    genres_prefer = [
        SurveyGenre(genre_id=prefer_id, is_liked=True) for prefer_id in prefer_ids
    ]
    genres_avoid = [
        SurveyGenre(genre_id=avoid_id, is_liked=False) for avoid_id in avoid_ids
    ]
    genres = genres_prefer + genres_avoid
    return genres


def gather_survey_animes(anime_ids: list[int]) -> list[SurveyAnime]:
    return [SurveyAnime(shikimori_anime_id=anime_id) for anime_id in anime_ids]


def gather_survey_characters(character_ids: list[int]) -> list[SurveyCharacter]:
    return [
        SurveyCharacter(shikimori_character_id=character_id)
        for character_id in character_ids
    ]


def gather_survey_read_dto(
    db_survey: Survey, dto: SurveyCreateDTO | SurveyUpdateDTO
) -> SurveyReadDTO:
    return SurveyReadDTO(
        id=db_survey.id,
        user_id=db_survey.user_id,
        created_at=db_survey.created_at,
        updated_at=db_survey.updated_at,
        genres_prefer=dto["genres_prefer"],
        genres_avoid=dto["genres_avoid"],
        animes_prefer=dto["animes_prefer"],
        characters_prefer=dto["characters_prefer"],
    )


def gather_survey_read_dto_from_orm(db_survey: Survey) -> SurveyReadDTO:
    genres_prefer = [genre.genre_id for genre in db_survey.genres if genre.is_liked]
    genres_avoid = [genre.genre_id for genre in db_survey.genres if not genre.is_liked]
    animes_prefer = [anime.id for anime in db_survey.animes]
    characters_prefer = [
        survey_character.character_id for survey_character in db_survey.characters
    ]

    return SurveyReadDTO(
        id=db_survey.id,
        user_id=db_survey.user_id,
        created_at=db_survey.created_at,
        updated_at=db_survey.updated_at,
        genres_prefer=genres_prefer,
        genres_avoid=genres_avoid,
        animes_prefer=animes_prefer,
        characters_prefer=characters_prefer,
    )


async def get_survey(session: AsyncSession, user_id: int) -> SurveyReadDTO | None:
    survey_result = await session.execute(
        select(Survey)
        .where(Survey.user_id == user_id)
        .options(
            selectinload(Survey.genres),
            selectinload(Survey.animes),
            selectinload(Survey.characters),
        )
    )
    db_survey = survey_result.scalar_one_or_none()

    if db_survey is None:
        return None

    return gather_survey_read_dto_from_orm(db_survey)


async def add_survey(session: AsyncSession, dto: SurveyCreateDTO) -> SurveyReadDTO:
    genres = gather_survey_genres(dto["genres_prefer"], dto["genres_avoid"])
    animes = gather_survey_animes(dto["animes_prefer"])
    characters = gather_survey_characters(dto["characters_prefer"])
    db_survey = Survey(
        user_id=dto["user_id"], genres=genres, animes=animes, characters=characters
    )

    session.add(db_survey)

    try:
        await session.flush()
    except IntegrityError:
        raise SurveyAlreadyExistsError

    await session.refresh(db_survey)

    return gather_survey_read_dto(db_survey, dto)


async def modify_survey(
    session: AsyncSession, dto: SurveyUpdateDTO
) -> SurveyReadDTO | None:
    genres = gather_survey_genres(dto["genres_prefer"], dto["genres_avoid"])
    animes = gather_survey_animes(dto["animes_prefer"])
    characters = gather_survey_characters(dto["characters_prefer"])

    survey_result = await session.execute(
        select(Survey)
        .where(Survey.user_id == dto["user_id"])
        .options(
            selectinload(Survey.genres),
            selectinload(Survey.animes),
            selectinload(Survey.characters),
        )
    )
    db_survey = survey_result.scalar_one_or_none()

    if db_survey is None:
        return None

    db_survey.genres = genres
    db_survey.animes = animes
    db_survey.characters = characters

    await session.flush()
    await session.refresh(db_survey)

    return gather_survey_read_dto(db_survey, dto)
