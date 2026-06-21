import typing
from datetime import date, time

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, int_pk, int_uniq

if typing.TYPE_CHECKING:
    from . import AnimeSynonym, Genre, Studio, Survey, WatchedAnime


class Anime(Base):
    __tablename__ = "animes"

    id: Mapped[int_pk]
    mal_id: Mapped[int_uniq]

    name: Mapped[str]
    english: Mapped[str | None]
    japanese: Mapped[str | None]

    poster_url: Mapped[str | None]
    synopsis: Mapped[str | None]

    score: Mapped[float | None]
    rank: Mapped[int | None]
    popularity: Mapped[int | None]
    nsfw: Mapped[str | None]
    kind: Mapped[str] = mapped_column(server_default="unknown")
    status: Mapped[str | None]
    episodes: Mapped[int] = mapped_column(server_default=sa.text("0"))
    source: Mapped[str | None]
    average_episode_duration: Mapped[int | None]

    aired_on: Mapped[date | None]
    released_on: Mapped[date | None]
    aired_year: Mapped[int | None]
    season: Mapped[str | None]

    broadcast_day: Mapped[str | None]
    broadcast_time: Mapped[time | None]

    genres: Mapped[list["Genre"]] = relationship(
        secondary="anime_genres", back_populates="animes"
    )
    studios: Mapped[list["Studio"]] = relationship(
        secondary="anime_studios", back_populates="animes"
    )
    surveys: Mapped[list["Survey"]] = relationship(
        secondary="survey_animes", back_populates="animes"
    )
    synonyms: Mapped[list["AnimeSynonym"]] = relationship(
        back_populates="anime", cascade="all, delete-orphan"
    )
    watched_entries: Mapped[list["WatchedAnime"]] = relationship(back_populates="anime")
