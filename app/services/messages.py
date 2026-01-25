from typing import Annotated

from fastapi import Depends

from app.models import Messages
from app.repositories.messages import MessagesRepository
from app.schemas.messages import MessageCreate


class MessagesService:
    def __init__(self, repository: Annotated[MessagesRepository, Depends()]):
        self._repository = repository

    async def get_all(self, chat_id: int):
        return await self._repository.get_all(chat_id)

    async def create(self, message: MessageCreate):
        message_db = Messages(**message.model_dump())
        return await self._repository.create(message_db)
