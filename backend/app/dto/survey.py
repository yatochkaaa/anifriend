from datetime import datetime
from typing import TypedDict


class SurveyBaseDTO(TypedDict):
    genres_prefer: list[int]
    genres_avoid: list[int]
    animes_prefer: list[int]
    characters_prefer: list[int]


class SurveyCreateDTO(SurveyBaseDTO):
    user_id: int


class SurveyUpdateDTO(SurveyBaseDTO):
    pass


class SurveyReadDTO(SurveyBaseDTO):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
