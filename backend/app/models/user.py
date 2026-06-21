import typing
from datetime import date

from sqlalchemy import Index, column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, int_pk, str_col, str_uniq

if typing.TYPE_CHECKING:
    from . import Survey, WatchedAnime


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("uq_users_username_lower", func.lower(column("username")), unique=True),
    )

    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    username: Mapped[str_col]
    hashed_password: Mapped[str]
    date_of_birth: Mapped[date | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    survey: Mapped["Survey | None"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    watched_animes: Mapped[list["WatchedAnime"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
