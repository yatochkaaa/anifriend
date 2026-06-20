import typing
from datetime import date

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, int_pk, int_uniq

if typing.TYPE_CHECKING:
    from . import Genre


class Anime(Base):
    __tablename__ = "animes"

    id: Mapped[int_pk]
    mal_id: Mapped[int_uniq]

    name: Mapped[str]
    english: Mapped[str | None]
    japanese: Mapped[str | None]

    poster_url: Mapped[str | None]

    score: Mapped[float | None]
    kind: Mapped[str] = mapped_column(server_default="unknown")
    status: Mapped[str | None]
    episodes: Mapped[int] = mapped_column(server_default=sa.text("0"))
    rank: Mapped[int | None]
    popularity: Mapped[int | None]
    nsfw: Mapped[str | None]
    aired_on: Mapped[date | None]
    released_on: Mapped[date | None]
    aired_year: Mapped[int | None]
    season: Mapped[str | None]

    raw: Mapped[dict] = mapped_column(JSONB, default=dict)

    genres: Mapped[list["Genre"]] = relationship(
        secondary="anime_genres", back_populates="animes"
    )
