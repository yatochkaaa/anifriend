from typing import Literal, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.dto import UserCreateDTO, UserUpdateDTO


async def get_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.get(User, user_id)
    return result


async def add_user(
    session: AsyncSession,
    dto: UserCreateDTO,
) -> User:
    db_user = User(**dto)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def modify_user(
    session: AsyncSession, user_id: int, dto: UserUpdateDTO
) -> User | None:
    db_user = await session.get(User, user_id)

    if not db_user:
        return None

    for key, value in dto.items():
        setattr(db_user, key, value)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def remove_user(session: AsyncSession, user_id: int) -> Literal[True] | None:
    db_user = await session.get(User, user_id)

    if not db_user:
        return None

    await session.delete(db_user)
    await session.commit()

    return True
