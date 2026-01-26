from pydantic import BaseModel

from app.models.chats import ChatType


class ChatInDB(BaseModel):
    title: str
    type: ChatType


class ChatCreate(BaseModel):
    title: str
    type: ChatType
    user_id_consumer: int
