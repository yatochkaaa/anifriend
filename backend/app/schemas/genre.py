from pydantic import BaseModel, ConfigDict


class GenreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    shikimori_id: int
    kind: str
    name: str
    russian: str
