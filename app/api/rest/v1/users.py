from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies.users import get_current_auth_user
from app.schemas.users import UserCreate, UserSchema
from app.services.users import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserSchema],
    dependencies=[Depends(get_current_auth_user)],
)
async def get_all(users_service: Annotated[UsersService, Depends()]):
    return await users_service.get_all()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    users_service: Annotated[UsersService, Depends()],
    user: UserCreate,
):
    return await users_service.create(user)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def me(
    users_service: Annotated[UsersService, Depends()],
    current_user: Annotated[
        UserSchema,
        Depends(get_current_auth_user),
    ],
):
    return await users_service.get_one(str(current_user.email))
