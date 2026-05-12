from fastapi import FastAPI

from app.api.main import api_v1_router
from app.core.config import settings

app = FastAPI()

app.include_router(api_v1_router, prefix=settings.API_V1_STR, tags=["v1"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}
