from fastapi import APIRouter

router = APIRouter(prefix="/survey", tags=["survey"])


@router.get("/")
async def get_survey():
    return {}
