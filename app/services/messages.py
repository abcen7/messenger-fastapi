from app.models import Messages
from app.repositories.messages import MessagesRepository
from app.schemas.messages import MessageCreate


class MessagesService:
    repository = MessagesRepository()

    async def get_history(self, chat_id: int):
        return await self.repository.get_all(chat_id)

    async def create_message(self, message: MessageCreate):
        message_db = Messages(**message.model_dump())
        return await self.repository.create(message_db)
