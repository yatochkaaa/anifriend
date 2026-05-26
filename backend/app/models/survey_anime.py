import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from . import Survey


class SurveyAnime(Base):
    """Favourite anime titles selected during onboarding survey."""

    __tablename__ = "survey_animes"

    survey_id: Mapped[int] = mapped_column(
        ForeignKey("surveys.id", ondelete="CASCADE"), primary_key=True
    )
    shikimori_anime_id: Mapped[int] = mapped_column(primary_key=True)

    survey: Mapped["Survey"] = relationship(back_populates="animes")
