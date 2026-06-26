import typing

from sqlalchemy.orm import Mapped, relationship

from .base import Base, int_pk, int_uniq

if typing.TYPE_CHECKING:
    from . import Anime, SurveyGenre


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int_pk]
    mal_id: Mapped[int_uniq]
    name: Mapped[str]

    surveys: Mapped[list["SurveyGenre"]] = relationship(
        back_populates="genre", cascade="all, delete-orphan"
    )
    animes: Mapped[list["Anime"]] = relationship(
        secondary="anime_genres", back_populates="genres"
    )
