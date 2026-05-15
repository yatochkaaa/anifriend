from sqlalchemy.ext.asyncio import AsyncSession

from app.dto import SurveyCreateDTO, SurveyReadDTO
from app.models import Survey, SurveyAnime, SurveyCharacter, SurveyGenre


async def add_survey(session: AsyncSession, dto: SurveyCreateDTO) -> SurveyReadDTO:
    genres_prefer = [
        SurveyGenre(genre_id=genre_id, is_liked=True)
        for genre_id in dto["genres_prefer"]
    ]
    genres_avoid = [
        SurveyGenre(genre_id=genre_id, is_liked=False)
        for genre_id in dto["genres_avoid"]
    ]
    genres = genres_prefer + genres_avoid
    animes = [
        SurveyAnime(shikimori_anime_id=anime_id) for anime_id in dto["animes_prefer"]
    ]
    characters = [
        SurveyCharacter(shikimori_character_id=character_id)
        for character_id in dto["characters_prefer"]
    ]

    db_survey = Survey(
        user_id=dto["user_id"], genres=genres, animes=animes, characters=characters
    )

    session.add(db_survey)
    await session.commit()
    await session.refresh(db_survey)

    survey_read: SurveyReadDTO = {
        "id": db_survey.id,
        "user_id": db_survey.user_id,
        "created_at": db_survey.created_at,
        "updated_at": db_survey.updated_at,
        "genres_prefer": dto["genres_prefer"],
        "genres_avoid": dto["genres_avoid"],
        "animes_prefer": dto["animes_prefer"],
        "characters_prefer": dto["characters_prefer"],
    }

    return survey_read
