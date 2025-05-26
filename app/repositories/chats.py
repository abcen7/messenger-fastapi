from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session
from app.models import ChatMember


class ChatsRepository:
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
