import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk

if typing.TYPE_CHECKING:
    from . import SurveyAnime, SurveyCharacter, SurveyGenre, User


class Survey(Base):
    """One-time onboarding survey capturing user's initial preferences."""

    __tablename__ = "surveys"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    animes: Mapped[list["SurveyAnime"]] = relationship(back_populates="survey")
    characters: Mapped[list["SurveyCharacter"]] = relationship(back_populates="survey")
    genres: Mapped[list["SurveyGenre"]] = relationship(back_populates="survey")
    user: Mapped["User"] = relationship(back_populates="survey")
