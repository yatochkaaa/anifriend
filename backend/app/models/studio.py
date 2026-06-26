import typing

from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base, int_pk, int_uniq

if typing.TYPE_CHECKING:
    from . import Anime


class Studio(Base):
    __tablename__ = "studios"

    id: Mapped[int_pk]
    mal_id: Mapped[int_uniq]
    name: Mapped[str]

    animes: Mapped[list["Anime"]] = relationship(
        secondary="anime_studios", back_populates="studios"
    )
