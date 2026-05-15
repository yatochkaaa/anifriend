import typing
from enum import StrEnum, auto

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IntrospectedEnum, int_pk, int_uniq

if typing.TYPE_CHECKING:
    from . import SurveyGenre


class GenreKindEnum(StrEnum):
    DEMOGRAPHIC = auto()
    GENRE = auto()
    THEME = auto()


class Genre(Base):
    """Anime genre cached from Shikimori API."""

    __tablename__ = "genres"

    id: Mapped[int_pk]
    shikimori_id: Mapped[int_uniq]
    name: Mapped[str]
    russian: Mapped[str]
    kind: Mapped[GenreKindEnum] = mapped_column(IntrospectedEnum(GenreKindEnum))

    surveys: Mapped[list["SurveyGenre"]] = relationship(back_populates="genre")
