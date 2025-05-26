from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session
from app.models import Users
from app.schemas.users import UserInDB


class UsersRepository:
    @with_async_session
    async def get_one(self, user_id: int, session: AsyncSession) -> Users | None:
        query = await session.execute(select(Users).where(Users.id == user_id))
        return query.scalar_one_or_none()

    @with_async_session
    async def get_one_by_email(self, email: str, session: AsyncSession) -> Users | None:
        query = await session.execute(select(Users).where(Users.email == email))
        return query.scalar_one_or_none()

    @with_async_session
    async def create(self, user: UserInDB, session: AsyncSession) -> None:
        session.add(user)
        await session.commit()

    @with_async_session
    async def get_all(self, session: AsyncSession) -> Sequence[Users]:
        query = await session.execute(select(Users))
        return query.scalars().all()
