import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk

if typing.TYPE_CHECKING:
    from . import Anime, SurveyGenre, User


class Survey(Base):
    """One-time onboarding survey capturing user's initial preferences."""

    __tablename__ = "surveys"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    animes: Mapped[list["Anime"]] = relationship(
        secondary="survey_animes", back_populates="surveys"
    )
    genres: Mapped[list["SurveyGenre"]] = relationship(
        back_populates="survey", cascade="all, delete-orphan"
    )

    user: Mapped["User"] = relationship(back_populates="survey")
