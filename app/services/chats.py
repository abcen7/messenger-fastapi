from app.repositories.chats import ChatsRepository
from app.schemas.chats import ChatCreate


class ChatsService:
    repository = ChatsRepository()

    async def is_member(
        self,
        *,
        chat_id: int,
        user_id: int,
    ) -> bool:
        return await self.repository.is_member(chat_id=chat_id, user_id=user_id)

    async def create(self, user_id_producer: int, chat: ChatCreate):
        return await self.repository.create(user_id_producer, chat)
