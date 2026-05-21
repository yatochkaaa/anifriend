from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.core.security import get_password_hash
from app.dto import UserCreateDTO, UserUpdateDTO
from app.exceptions import UserAlreadyExistsError
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services import (
    add_user,
    get_user_by_id,
    get_users,
    modify_user,
    remove_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users(session: SessionDep) -> list[UserRead]:
    users = await get_users(session)
    return [UserRead.model_validate(user) for user in users]


@router.get("/{user_id}")
async def read_user(user_id: int, session: SessionDep) -> UserRead:
    user = await get_user_by_id(session, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserRead.model_validate(user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: SessionDep) -> UserRead:
    hashed_password = get_password_hash(user.password)
    dto = UserCreateDTO(
        email=str(user.email).lower(),
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
    )

    try:
        created_user = await add_user(session, dto)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already taken")

    return UserRead.model_validate(created_user)


@router.patch("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, session: SessionDep) -> UserRead:
    update_data = user.model_dump(exclude_unset=True)
    dto = UserUpdateDTO(**update_data)
    updated_user = await modify_user(session, user_id, dto)

    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserRead.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep) -> None:
    result = await remove_user(session, user_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
