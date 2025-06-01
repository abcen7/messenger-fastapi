from typing import Sequence

from fastapi import HTTPException
from starlette import status

from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import UserCreate, UserInDB, UserLogin
from app.utils.auth import AuthHelper


class UsersService:
    repository = UsersRepository()

    async def create(self, user: UserCreate) -> None:
        if (
            await self.repository.get_one_or_none(
                self.repository.model.email == user.email
            )
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists",
            )
        user_create_dto = UserInDB(
            **user.model_dump(),
            hashed_password=AuthHelper.get_password_hash(user.password),
        )
        await self.repository.create(user_create_dto)

    async def get_all(self) -> Sequence[Users]:
        return await self.repository.get_all()

    async def get_one(self, email: str) -> Users:
        if (
            user := await self.repository.get_one(self.repository.model.email == email)
        ) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
