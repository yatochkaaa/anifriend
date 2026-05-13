from typing import TypedDict
from datetime import date


class UserCreateDTO(TypedDict):
    email: str
    username: str
    hashed_password: str
    first_name: str | None
    last_name: str | None
    date_of_birth: date | None


class UserUpdateDTO(TypedDict, total=False):
    email: str
    username: str
    first_name: str | None
    last_name: str | None
    date_of_birth: date | None
