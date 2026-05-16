from pydantic import BaseModel, ConfigDict


class PosterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    main_url: str | None = None


class AnimeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    russian: str | None
    score: float | None
    poster: PosterRead | None
