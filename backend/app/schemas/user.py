from datetime import date, datetime
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserPasswordMixin:
    password: Annotated[str, Field(min_length=8, max_length=100)]
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None


class UserCreate(UserPasswordMixin, UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
