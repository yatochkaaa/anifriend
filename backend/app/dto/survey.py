from datetime import datetime
from typing import TypedDict


class SurveyGenreDTO(TypedDict):
    genre_id: int
    is_liked: bool


class SurveyBaseDTO(TypedDict):
    genres: list[SurveyGenreDTO]
    animes: list[int]


class SurveyCreateDTO(SurveyBaseDTO):
    user_id: int


class SurveyUpdateDTO(SurveyBaseDTO):
    user_id: int


class SurveyReadDTO(SurveyBaseDTO):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
