from datetime import datetime

from pydantic import BaseModel


class SurveyBase(BaseModel):
    genres_prefer: list[int]
    genres_avoid: list[int]
    animes_prefer: list[int]
    characters_prefer: list[int]


class SurveyCreate(SurveyBase):
    pass


class SurveyRead(SurveyBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class SurveyUpdate(SurveyBase):
    pass
