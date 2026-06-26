from datetime import date
from typing import TypedDict


class UserCreateDTO(TypedDict):
    email: str
    username: str
    hashed_password: str
    date_of_birth: date | None


class UserUpdateDTO(TypedDict, total=False):
    email: str
    username: str
    date_of_birth: date | None
