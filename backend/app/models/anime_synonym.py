import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, int_pk

if typing.TYPE_CHECKING:
    from . import Anime


class AnimeSynonym(Base):
    __tablename__ = "anime_synonyms"

    id: Mapped[int_pk]
    anime_id: Mapped[int] = mapped_column(
        ForeignKey("animes.id", ondelete="CASCADE")
    )
    value: Mapped[str]

    anime: Mapped["Anime"] = relationship(back_populates="synonyms")
