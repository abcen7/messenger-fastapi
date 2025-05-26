from app.repositories.messages import MessagesRepository


class MessagesService:
    repository = MessagesRepository()

    async def get_history(self, chat_id: int):
        return await self.repository.get_all(chat_id)
