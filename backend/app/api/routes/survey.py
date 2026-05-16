from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.dto import SurveyCreateDTO, SurveyUpdateDTO
from app.schemas import SurveyCreate, SurveyRead, SurveyUpdate
from app.services.survey import add_survey, modify_survey

router = APIRouter(prefix="/survey", tags=["survey"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_survey(survey: SurveyCreate, session: SessionDep) -> SurveyRead:
    dto = SurveyCreateDTO(
        #  TODO: replace with current user from JWT
        user_id=1,
        genres_prefer=survey.genres_prefer,
        genres_avoid=survey.genres_avoid,
        animes_prefer=survey.animes_prefer,
        characters_prefer=survey.characters_prefer,
    )
    created_survey = await add_survey(session, dto)

    return SurveyRead.model_validate(created_survey)


@router.put("/")
async def update_survey(survey: SurveyUpdate, session: SessionDep) -> SurveyRead:
    dto = SurveyUpdateDTO(
        #  TODO: replace with current user from JWT
        user_id=1,
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
