from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.core.security import create_access_token, get_password_hash
from app.dto import UserCreateDTO
from app.exceptions import UserAlreadyExistsError
from app.schemas import Token, UserCreate
from app.services import add_user, authenticate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, session: SessionDep) -> Token:
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already taken",
        )

    access_token = create_access_token(
        {"sub": str(created_user.id), "username": created_user.username}
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = await authenticate(
        session, username_or_email=form_data.username, password=form_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id), "username": user.username})

    return Token(access_token=access_token, token_type="bearer")
