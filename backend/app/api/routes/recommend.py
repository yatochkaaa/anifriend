from fastapi import APIRouter

from app.api.deps import CurrentUserDep, SessionDep, ShikimoriDep
from app.schemas import AnimeRead
from app.services import get_recommendations

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/")
async def read_recommendations(
    session: SessionDep, shikimori_client: ShikimoriDep, current_user: CurrentUserDep
) -> list[AnimeRead]:
    recommendations = await get_recommendations(session, shikimori_client, current_user.id)
    return [AnimeRead.model_validate(recommend) for recommend in recommendations]
