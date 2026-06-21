import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if typing.TYPE_CHECKING:
    from . import Survey


class SurveyCharacter(Base):
    """Favourite characters selected during onboarding survey."""

    __tablename__ = "survey_characters"

    survey_id: Mapped[int] = mapped_column(
        ForeignKey("surveys.id", ondelete="CASCADE"), primary_key=True
    )
    character_id: Mapped[int] = mapped_column(primary_key=True)

    survey: Mapped["Survey"] = relationship(back_populates="characters")
