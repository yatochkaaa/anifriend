import typing
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk, str_uniq

if typing.TYPE_CHECKING:
    from . import Survey, WatchedAnime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    username: Mapped[str_uniq]
    hashed_password: Mapped[str]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    date_of_birth: Mapped[date | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    survey: Mapped["Survey | None"] = relationship(back_populates="user")
    watched_animes: Mapped[list["WatchedAnime"]] = relationship(back_populates="user")
