from pydantic import BaseModel


class WebsocketReceiveMessage(BaseModel):
    text: str


class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    text: str


class ReadMessage(BaseModel):
    message_id: int
    user_id: int
