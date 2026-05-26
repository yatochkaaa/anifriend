import typing
from enum import StrEnum, auto

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IntrospectedEnum

if typing.TYPE_CHECKING:
    from . import User


class WatchedAnimeStatus(StrEnum):
    PLANNED = auto()
    WATCHING = auto()
    REWATCHING = auto()
    COMPLETED = auto()
    ON_HOLD = auto()
    DROPPED = auto()


class WatchedAnime(Base):
    """User's anime tracking list with watch status, rating, and whether the title was recommended by the system."""

    __tablename__ = "watched_animes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    shikimori_anime_id: Mapped[int] = mapped_column(primary_key=True)
    rating: Mapped[float | None] = mapped_column(default=None)
    status: Mapped[WatchedAnimeStatus | None] = mapped_column(
        IntrospectedEnum(WatchedAnimeStatus), default=None
    )
    is_recommended: Mapped[bool | None] = mapped_column(default=None)

    user: Mapped["User"] = relationship(back_populates="watched_animes")
