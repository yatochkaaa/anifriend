from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas import GenreRead
from app.services import get_genres

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/")
async def read_genres(session: SessionDep) -> list[GenreRead]:
    genres = await get_genres(session)

    return [GenreRead.model_validate(genre) for genre in genres]
