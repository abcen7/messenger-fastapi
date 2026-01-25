from typing import Annotated, Sequence

from fastapi import Depends, HTTPException
from starlette import status

from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import UserCreate, UserInDB
from app.utils.auth import AuthHelper


class UsersService:
    def __init__(self, repository: Annotated[UsersRepository, Depends()]):
        self._repository = repository

    async def create(self, user: UserCreate) -> None:
        if self._repository.is_exists_by_email(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        user_create_dto = UserInDB(
            **user.model_dump(),
            hashed_password=AuthHelper.get_password_hash(user.password),
        )
        await self._repository.create(user_create_dto)

    async def get_all(self) -> Sequence[Users]:
        return await self._repository.get_all()

    async def get_one(self, email: str) -> Users:
        if (user := await self._repository.get_by_email(email)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
