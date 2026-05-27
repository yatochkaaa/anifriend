from datetime import datetime

from pydantic import BaseModel, Field


class SurveyCreate(BaseModel):
    genres_prefer: list[int] = Field(max_length=5)
    genres_avoid: list[int]
    animes_prefer: list[int]
    characters_prefer: list[int]


class SurveyRead(BaseModel):
    id: int
    user_id: int
    genres_prefer: list[int]
    genres_avoid: list[int]
    animes_prefer: list[int]
    characters_prefer: list[int]
    created_at: datetime
    updated_at: datetime


class SurveyUpdate(SurveyCreate):
    pass
