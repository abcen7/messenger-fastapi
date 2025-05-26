from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    text: str
