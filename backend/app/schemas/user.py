from datetime import date
from typing_extensions import Self

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class UserPasswordMixin:
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


class UserBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    email: EmailStr
    username: str


class UserCreate(UserBase, UserPasswordMixin):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool


class UserUpdate(UserBase):
    email: EmailStr | None = None
    username: str | None = None
