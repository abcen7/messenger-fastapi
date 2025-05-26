from app.models import Messages, MessagesRead
from app.repositories.messages import MessagesRepository
from app.schemas.messages import MessageCreate, ReadMessage


class MessagesService:
    repository = MessagesRepository()

    async def get_history(self, chat_id: int):
        return await self.repository.get_all(chat_id)

    async def create_message(self, message: MessageCreate):
        message_db = Messages(**message.model_dump())
        return await self.repository.create(message_db)

    async def read_message(self, message: ReadMessage):
        message_read_db = MessagesRead(**message.model_dump())
        return await self.repository.read_message(message_read_db)
