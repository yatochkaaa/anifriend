from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUserDep, SessionDep
from app.dto import UserUpdateDTO
from app.exceptions import UserAlreadyExistsError
from app.schemas import UserRead, UserUpdate
from app.services import (
    get_user_by_id,
    get_users,
    modify_user,
    remove_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def read_user(user_id: int, session: SessionDep) -> UserRead:
    user = await get_user_by_id(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserRead.model_validate(user)


@router.get("/")
async def read_users(session: SessionDep) -> list[UserRead]:
    users = await get_users(session)
    return [UserRead.model_validate(user) for user in users]


@router.patch("/me")
async def update_user_me(
    current_user: CurrentUserDep,
    data: UserUpdate,
    session: SessionDep,
) -> UserRead:
    update_data = data.model_dump(exclude_unset=True)
    dto = UserUpdateDTO(**update_data)

    try:
        updated_user = await modify_user(session, current_user.id, dto)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already taken",
        )

    await session.commit()
    await session.refresh(updated_user)

    return UserRead.model_validate(updated_user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(current_user: CurrentUserDep, session: SessionDep) -> None:
    await remove_user(session, current_user.id)
    await session.commit()
