from typing import Annotated

from fastapi import Depends

from app.repositories.chats import ChatsRepository
from app.schemas.chats import ChatCreate


class ChatsService:
    def __init__(self, repository: Annotated[ChatsRepository, Depends()]):
        self._repository = repository

    async def is_member(
        self,
        *,
        chat_id: int,
        user_id: int,
    ) -> bool:
        return await self._repository.is_member(chat_id=chat_id, user_id=user_id)

    async def create(self, user_id_producer: int, chat: ChatCreate):
        return await self._repository.create_and_invite(user_id_producer, chat)

    async def get_all(self, user_id: int):
        return await self._repository.get_all_by_user_id(user_id)
