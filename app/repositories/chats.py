from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session


class ChatsRepository:
    @with_async_session
    async def is_member(
        self, chat_id: int, user_id: int, session: AsyncSession
    ) -> bool:
        pass
        # stmt = select(GroupMember).where(
        #     GroupMember.group_id == chat_id, GroupMember.user_id == user_id
        # )
        # result = await session.execute(stmt)
        # return result.scalar_one_or_none() is not None
