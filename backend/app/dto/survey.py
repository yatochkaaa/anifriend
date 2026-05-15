from typing import TypedDict


class SurveyCreateDTO(TypedDict):
    user_id: int
    genres_prefer: list[int]
    genres_avoid: list[int]
    animes_prefer: list[int]
    characters_prefer: list[int]


class SurveyUpdateDTO(TypedDict):
    genres_prefer: list[int]
    genres_avoid: list[int]
    animes_prefer: list[int]
    characters_prefer: list[int]
