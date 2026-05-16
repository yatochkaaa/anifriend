from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.db import async_session_maker
from app.integrations import ShikimoriClient


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_shikimori_client(request: Request) -> ShikimoriClient:
    return request.app.state.shikimori_client


SessionDep = Annotated[AsyncSession, Depends(get_db)]
ShikimoriDep = Annotated[ShikimoriClient, Depends(get_shikimori_client)]
