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
        print(user)
        if await self.repository.get_one_by_email(user.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User already exists",
            )
        user_db_model = Users(
            **UserInDB(
                **user.model_dump(),
                hashed_password=AuthHelper.get_password_hash(user.password),
            ).model_dump()
        )
        await self.repository.create(user_db_model)

    async def get_all(self) -> Sequence[Users]:
        return await self.repository.get_all()

    async def get_one(self, email: str) -> Users:
        if (user := await self.repository.get_one_by_email(email)) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
