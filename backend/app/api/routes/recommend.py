from fastapi import APIRouter

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/")
async def get_recommend():
    return {}
