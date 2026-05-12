from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, int_pk, str_uniq


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    date_of_birth: Mapped[date | None]
    email: Mapped[str_uniq]
    username: Mapped[str_uniq]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
