from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SurveyGenreCreate(BaseModel):
    genre_id: int = Field(validation_alias="id")
    is_liked: bool


class SurveyGenreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(validation_alias="genre_id")
    is_liked: bool


class SurveyCreate(BaseModel):
    genres: list[SurveyGenreCreate]
    animes: list[int]


class SurveyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    genres: list[SurveyGenreRead]
    animes: list[int]
    created_at: datetime
    updated_at: datetime

    @field_validator("animes", mode="before")
    @classmethod
    def _animes_to_ids(cls, v) -> list[int]:
        return [a.id for a in v]


class SurveyUpdate(SurveyCreate):
    pass
