from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserDep, SessionDep
from app.dto import SurveyCreateDTO, SurveyUpdateDTO
from app.schemas import SurveyCreate, SurveyRead, SurveyUpdate
from app.services import add_survey, get_survey, modify_survey

router = APIRouter(prefix="/survey", tags=["survey"])


@router.get("/")
async def read_survey(session: SessionDep, current_user: CurrentUserDep) -> SurveyRead:
    survey = await get_survey(session, current_user.id)

    if survey is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found"
        )

    return SurveyRead.model_validate(survey)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_survey(
    survey: SurveyCreate, session: SessionDep, current_user: CurrentUserDep
) -> SurveyRead:
    dto = SurveyCreateDTO(
        user_id=current_user.id,
        genres_prefer=survey.genres_prefer,
        genres_avoid=survey.genres_avoid,
        animes_prefer=survey.animes_prefer,
        characters_prefer=survey.characters_prefer,
    )
    created_survey = await add_survey(session, dto)

    return SurveyRead.model_validate(created_survey)


@router.put("/")
async def update_survey(
    survey: SurveyUpdate, session: SessionDep, current_user: CurrentUserDep
) -> SurveyRead:
    dto = SurveyUpdateDTO(
        user_id=current_user.id,
        genres_prefer=survey.genres_prefer,
        genres_avoid=survey.genres_avoid,
        animes_prefer=survey.animes_prefer,
        characters_prefer=survey.characters_prefer,
    )
    updated_survey = await modify_survey(session, dto)

    if updated_survey is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Survey not found"
        )

    return SurveyRead.model_validate(updated_survey)
