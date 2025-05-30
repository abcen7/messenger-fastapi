from typing import Sequence

from sqlalchemy import func, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session
from app.models import ChatMember, Chats
from app.models.chats import ChatType
from app.schemas.chats import ChatCreate


class ChatsRepository:
    @with_async_session
    async def get_one(
        self,
        *,
        user_id_consumer: int,
        user_id_producer: int,
        session: AsyncSession,
    ) -> int:
        query = await session.execute(
            select(ChatMember.chat_id)
            .join(Chats, Chats.id == ChatMember.chat_id)
            .where(
                Chats.type == ChatType.PRIVATE,
                ChatMember.user_id.in_([user_id_consumer, user_id_producer]),
            )
            .group_by(ChatMember.chat_id)
            .having(func.count(func.distinct(ChatMember.user_id)) == 2)
        )
        return query.scalar()

    @with_async_session
    async def is_member(
        self,
        *,
        chat_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> bool:
        query = await session.execute(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id,
            )
        )
        return query.scalar_one_or_none() is not None

    @with_async_session
    async def create(
        self,
        user_id_producer,
        chat: ChatCreate,
        session: AsyncSession,
    ):
        pass
