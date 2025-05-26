from typing import Sequence

from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session
from app.models import Messages


class MessagesRepository:
    @with_async_session
    async def get_all(self, chat_id: int, session: AsyncSession) -> Sequence[Messages]:
        query = await session.execute(
            select(Messages)
            .where(Messages.chat_id == chat_id)
            .order_by(Messages.created_at.asc())
        )
        return query.scalars().all()
