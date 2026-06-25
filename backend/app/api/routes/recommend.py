from fastapi import APIRouter

from app.api.deps import CurrentUserDep, SessionDep
from app.schemas import AnimeRead
from app.services import get_recommendations

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/")
async def read_recommendations(
    session: SessionDep, current_user: CurrentUserDep
) -> list[AnimeRead]:
    recommendations = await get_recommendations(session, user_id=current_user.id)
    return [AnimeRead.model_validate(recommend) for recommend in recommendations]
