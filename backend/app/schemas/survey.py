from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class SurveyGenre(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    genre_id: int
    is_liked: bool


class SurveyCreate(BaseModel):
    genres: list[SurveyGenre]
    animes: list[int]


class SurveyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    genres: list[SurveyGenre]
    animes: list[int]
    created_at: datetime
    updated_at: datetime

    @field_validator("animes", mode="before")
    @classmethod
    def _animes_to_ids(cls, v) -> list[int]:
        return [a.id for a in v]


class SurveyUpdate(SurveyCreate):
    pass
