from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import SessionDep
from app.schemas import AnimeRead
from app.services import get_animes

router = APIRouter(prefix="/animes", tags=["animes"])


@router.get("/")
async def read_animes(
    session: SessionDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
    score_min: Annotated[int, Query(ge=1, le=10)] = 1,
    genre_ids: Annotated[list[int] | None, Query()] = None,
    search: str | None = None,
) -> list[AnimeRead]:
    animes = await get_animes(
        session,
        limit=limit,
        offset=offset,
        score_min=score_min,
        genre_ids=genre_ids,
        search=search,
    )

    return [AnimeRead.model_validate(anime) for anime in animes]
