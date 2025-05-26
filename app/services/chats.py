from app.repositories.chats import ChatsRepository


class ChatsService:
    repository = ChatsRepository()

    async def is_member(
        self,
        *,
        chat_id: int,
        user_id: int,
    ) -> bool:
        return await self.repository.is_member(chat_id=chat_id, user_id=user_id)
