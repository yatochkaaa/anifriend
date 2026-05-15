from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.api.main import api_v1_router
from app.core.config import settings
from app.integrations.shikimori import ShikimoriClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    client = httpx.AsyncClient()
    app.state.shikimori_client = ShikimoriClient(client)
    yield
    await client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
