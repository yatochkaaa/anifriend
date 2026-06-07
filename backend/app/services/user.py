from typing import Literal, Sequence

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.dto import UserCreateDTO, UserUpdateDTO
from app.exceptions import UserAlreadyExistsError
from app.models import User


async def get_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.get(User, user_id)
    return result


async def authenticate(
    session: AsyncSession, username_or_email: str, password: str
) -> User | None:
    search_term = username_or_email.strip().lower()

    stmt = select(User).where(
        or_(func.lower(User.username) == search_term, User.email == search_term)
    )
    result = await session.execute(stmt)
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


async def add_user(
    session: AsyncSession,
    dto: UserCreateDTO,
) -> User:
    db_user = User(**dto)
    session.add(db_user)

    try:
        await session.flush()
    except IntegrityError:
        raise UserAlreadyExistsError

    return db_user


async def modify_user(
    session: AsyncSession, user_id: int, dto: UserUpdateDTO
) -> User | None:
    db_user = await session.get(User, user_id)

    if not db_user:
        return None

    for key, value in dto.items():
        setattr(db_user, key, value)

    try:
        await session.flush()
    except IntegrityError:
        raise UserAlreadyExistsError

    return db_user


async def remove_user(session: AsyncSession, user_id: int) -> Literal[True] | None:
    db_user = await session.get(User, user_id)

    if not db_user:
        return None

    await session.delete(db_user)

    return True
