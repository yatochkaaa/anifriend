from fastapi import APIRouter

from app.api.deps import SessionDep, ShikimoriDep
from app.schemas import AnimeRead
from app.services import get_recommendations

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/")
async def read_recommendations(
    session: SessionDep, shikimori_client: ShikimoriDep
) -> list[AnimeRead]:
    recommendations = await get_recommendations(session, shikimori_client)
    return [AnimeRead.model_validate(recommend) for recommend in recommendations]
