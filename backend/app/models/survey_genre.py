import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from . import Genre, Survey


class SurveyGenre(Base):
    """Junction table linking survey to liked/disliked genres."""

    __tablename__ = "survey_genres"

    survey_id: Mapped[int] = mapped_column(
        ForeignKey("surveys.id", ondelete="CASCADE"), primary_key=True
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True
    )
    is_liked: Mapped[bool]

    survey: Mapped["Survey"] = relationship(back_populates="genres")
    genre: Mapped["Genre"] = relationship(back_populates="surveys")
