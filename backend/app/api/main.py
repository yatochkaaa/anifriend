from fastapi import APIRouter

from app.api.routes import auth, genres, recommend, survey, users

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(genres.router)
api_v1_router.include_router(recommend.router)
api_v1_router.include_router(survey.router)
api_v1_router.include_router(users.router)
