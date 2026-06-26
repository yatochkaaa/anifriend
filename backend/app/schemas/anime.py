from datetime import date, time

from pydantic import BaseModel, ConfigDict

from .genre import GenreRead


class PosterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    main_url: str | None = None


class AnimeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    english: str | None
    japanese: str | None

    poster_url: str | None
    synopsis: str | None

    score: float | None
    rank: int | None
    popularity: int | None
    nsfw: str | None
    kind: str
    status: str | None
    episodes: int
    source: str | None
    average_episode_duration: int | None

    aired_on: date | None
    released_on: date | None
    aired_year: int | None
    season: str | None

    broadcast_day: str | None
    broadcast_time: time | None

    genres: list[GenreRead]
