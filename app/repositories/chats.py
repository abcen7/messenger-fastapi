from typing import Any, Sequence

from sqlalchemy import ColumnExpressionArgument, func, select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session
from app.core.repositories import BaseRepository
from app.models import ChatMember, Chats
from app.models.chats import ChatType
from app.schemas.chats import ChatCreate, ChatInDB


class ChatsRepository(BaseRepository[Chats, ChatInDB]):
    _db_model = Chats

    # async def get_one(
    #     self,
    #     *,
    #     user_id_consumer: int,
    #     user_id_producer: int,
    # ) -> int:
    #     query = await self._session.execute(
    #         select(ChatMember.chat_id)
    #         .join(Chats, Chats.id == ChatMember.chat_id)
    #         .where(
    #             Chats.type == ChatType.PRIVATE,
    #             ChatMember.user_id.in_([user_id_consumer, user_id_producer]),
    #         )
    #         .group_by(ChatMember.chat_id)
    #         .having(func.count(func.distinct(ChatMember.user_id)) == 2)  # type: ignore
    #     )
    #     return query.scalar()

    async def is_member(
        self,
        *,
        chat_id: int,
        user_id: int,
    ) -> bool:
        query = await self._session.execute(
            select(ChatMember).where(
                ChatMember.chat_id == chat_id,
                ChatMember.user_id == user_id,
            )
        )
        return query.scalar_one_or_none() is not None

    async def get_all_by_user_id(self, user_id: int) -> list[Chats]:
        return await self.get_all(Chats.members.in_([user_id]))

    async def create_and_invite(
        self,
        user_id_producer: int,
        chat: ChatCreate,
    ) -> None:
        try:
            created_chat: Chats = await self.create(
                ChatInDB(
                    title=chat.title,
                    type=chat.type,
                )
            )
            producer_member = ChatMember(
                chat_id=created_chat.id,
                user_id=user_id_producer,
            )
            consumer_member = ChatMember(
                chat_id=created_chat.id,
                user_id=user_id_producer,
            )
            self._session.add(producer_member)
            self._session.add(consumer_member)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise e
