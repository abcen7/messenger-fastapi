from pydantic import BaseModel


class WebsocketReceiveMessage(BaseModel):
    text: str


class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    text: str
